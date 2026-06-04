"""
Dispatcher: Task Assignment and Dispatching Policies
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from .resources import Resource, ResourcePool
from .flow_generator import Task, TaskPriority


class DispatchPolicy(ABC):
    """Base class for dispatching policies"""
    
    def __init__(self, name: str):
        self.name = name
        self.decisions_made = 0
    
    @abstractmethod
    def select_resource(self, task: Task, pool: ResourcePool) -> Optional[Resource]:
        """Select best resource for task"""
        pass
    
    def __repr__(self):
        return f"{self.name} (decisions: {self.decisions_made})"


class FIFODispatcher(DispatchPolicy):
    """First-In-First-Out (FIFO) Policy
    
    Tasks are served in arrival order, regardless of type or priority.
    Baseline comparison policy.
    """
    
    def __init__(self):
        super().__init__("FIFO")
    
    def select_resource(self, task: Task, pool: ResourcePool) -> Optional[Resource]:
        """Select least busy resource (FIFO on all tasks)"""
        self.decisions_made += 1
        return pool.get_least_busy()


class PriorityDispatcher(DispatchPolicy):
    """Priority-Based Dispatcher
    
    Exceptional flows get priority over nominal flows.
    Within same flow type, urgent tasks prioritized.
    """
    
    def __init__(self):
        super().__init__("Priority-Based")
    
    def select_resource(self, task: Task, pool: ResourcePool) -> Optional[Resource]:
        """Assign based on task priority"""
        self.decisions_made += 1
        
        # Select fastest available resource for high-priority tasks
        if task.priority in [TaskPriority.URGENT, TaskPriority.HIGH]:
            resource = pool.get_fastest_available()
        else:
            # Use least busy for normal/low priority
            resource = pool.get_least_busy()
        
        return resource


class LoadBalancingDispatcher(DispatchPolicy):
    """Load Balancing Dispatcher
    
    Distributes work evenly across all resources to minimize queue length
    and improve throughput.
    """
    
    def __init__(self):
        super().__init__("Load-Balancing")
    
    def select_resource(self, task: Task, pool: ResourcePool) -> Optional[Resource]:
        """Always select least busy resource"""
        self.decisions_made += 1
        return pool.get_least_busy()


class PreemptiveDispatcher(DispatchPolicy):
    """Preemptive Priority Dispatcher
    
    Exceptional/urgent tasks can preempt normal tasks.
    High priority tasks get fastest available resource.
    Can pause low-priority tasks if needed.
    """
    
    def __init__(self):
        super().__init__("Preemptive")
        self.preemptions = 0
    
    def select_resource(self, task: Task, pool: ResourcePool) -> Optional[Resource]:
        """Select resource and potentially preempt lower-priority task"""
        self.decisions_made += 1
        
        if task.priority == TaskPriority.URGENT:
            # URGENT: Get fastest resource, may need to preempt
            best_resource = pool.get_fastest_available()
            
            # Check if preemption could help
            if best_resource.current_task and best_resource.current_task.priority in [TaskPriority.LOW, TaskPriority.NORMAL]:
                # In real system, preemption logic would be here
                # For now, just record that we would preempt
                self.preemptions += 1
            
            return best_resource
        
        elif task.priority == TaskPriority.HIGH:
            # HIGH: Use fastest available or least busy
            return pool.get_fastest_available()
        
        else:
            # NORMAL/LOW: Least busy resource
            return pool.get_least_busy()


class AdaptiveDispatcher(DispatchPolicy):
    """Adaptive Dispatcher
    
    Switches between strategies based on system state:
    - If queues are long: Load balance
    - If many urgent tasks: Priority-based
    - If queue short: Nearest resource
    """
    
    def __init__(self):
        super().__init__("Adaptive")
        self.mode = "balanced"
    
    def select_resource(self, task: Task, pool: ResourcePool) -> Optional[Resource]:
        """Adaptive selection based on system state"""
        self.decisions_made += 1
        
        # Assess system state
        avg_queue = pool.get_pool_stats()['total_queue_length'] / max(1, len(pool.resources))
        
        # Switch strategy based on queue depth
        if avg_queue > 3:
            # Queues getting long: Load balance strictly
            self.mode = "balanced"
            return pool.get_least_busy()
        elif task.priority in [TaskPriority.URGENT, TaskPriority.HIGH]:
            # Many urgent tasks: Prioritize
            self.mode = "priority"
            return pool.get_fastest_available()
        else:
            # Normal conditions: Standard balance
            self.mode = "balanced"
            return pool.get_least_busy()


class Dispatcher:
    """Main dispatcher coordinator"""
    
    def __init__(self, policy: DispatchPolicy, pool: ResourcePool):
        self.policy = policy
        self.pool = pool
        self.assignment_history = []
    
    def assign_task(self, task: Task) -> Resource:
        """Assign task to resource using current policy"""
        resource = self.policy.select_resource(task, self.pool)
        
        self.assignment_history.append({
            'task_id': task.task_id,
            'resource_id': resource.spec.resource_id,
            'policy': self.policy.name,
            'assignment_time': task.arrival_time,
        })
        
        task.assigned_resource = resource.spec.resource_id
        return resource
    
    def get_statistics(self) -> dict:
        """Get dispatcher statistics"""
        return {
            'policy': self.policy.name,
            'assignments': len(self.assignment_history),
            'decisions': self.policy.decisions_made,
        }


def create_dispatcher(policy_name: str, pool: ResourcePool) -> Dispatcher:
    """Factory function to create dispatcher by name"""
    
    policies = {
        'fifo': FIFODispatcher(),
        'priority': PriorityDispatcher(),
        'load_balancing': LoadBalancingDispatcher(),
        'preemptive': PreemptiveDispatcher(),
        'adaptive': AdaptiveDispatcher(),
    }
    
    policy = policies.get(policy_name.lower())
    if not policy:
        raise ValueError(f"Unknown policy: {policy_name}")
    
    return Dispatcher(policy, pool)
