"""
Resource Models: Heterogeneous Fleet Components
Defines automated, semi-automated, and manual resources for intralogistics
"""

import simpy
from typing import Optional
from dataclasses import dataclass


@dataclass
class ResourceSpec:
    """Specification for a resource"""
    resource_id: str
    resource_type: str  # 'automated', 'semi_automated', 'manual'
    speed: float  # tasks per hour or units per minute
    capacity: int  # max tasks in queue
    availability: float  # probability 0-1 (1.0 = always available)
    cost_per_hour: float  # operational cost
    max_payload: float  # weight capacity


class Resource:
    """Base Resource class for intralogistics"""
    
    def __init__(self, env: simpy.Environment, spec: ResourceSpec):
        self.env = env
        self.spec = spec
        self.resource = simpy.Resource(env, capacity=1)
        self.queue = []
        self.in_service = []
        self.idle_time = 0
        self.busy_time = 0
        self.num_completed = 0
        self.num_failed = 0
        self.current_task = None
        
    def process_task(self, task, duration: float):
        """Process a task for given duration"""
        return self.resource.request()
    
    def get_utilization(self) -> float:
        """Return resource utilization rate"""
        total_time = self.busy_time + self.idle_time + 1e-6
        return self.busy_time / total_time
    
    def get_queue_length(self) -> int:
        """Return current queue length"""
        return len(self.queue) + len(self.in_service)


class AutomatedResource(Resource):
    """Automated Resource (AGV, Automated Conveyor)
    - Fast processing
    - High reliability
    - Limited flexibility
    """
    
    def __init__(self, env: simpy.Environment, spec: ResourceSpec):
        super().__init__(env, spec)
        self.processing_time_factor = 0.5  # 50% faster than manual
        self.reliability = spec.availability
        
    def get_processing_time(self, task_weight: float) -> float:
        """Calculate processing time for task"""
        base_time = 60 / self.spec.speed  # minutes
        return base_time * self.processing_time_factor / (task_weight / 10 + 1)  # normalize for weight
    
    def is_available(self) -> bool:
        """Check if resource is available (reliability check)"""
        import random
        return random.random() < self.reliability


class SemiAutomatedResource(Resource):
    """Semi-Automated Resource (Motorized Conveyor, Robotic Arm)
    - Medium speed
    - Good throughput
    - Limited routing flexibility
    """
    
    def __init__(self, env: simpy.Environment, spec: ResourceSpec):
        super().__init__(env, spec)
        self.processing_time_factor = 0.8  # 20% faster than manual
        self.reliability = spec.availability * 0.95  # slightly less reliable
        
    def get_processing_time(self, task_weight: float) -> float:
        """Calculate processing time for task"""
        base_time = 60 / self.spec.speed  # minutes
        variability = 1.0 + (0.1 * (abs(task_weight - 10) / 10))  # add weight variability
        return base_time * self.processing_time_factor * variability
    
    def is_available(self) -> bool:
        """Check if resource is available"""
        import random
        return random.random() < self.reliability


class ManualResource(Resource):
    """Manual Resource (Human Operator)
    - Flexible
    - Variable processing times
    - Subject to fatigue, breaks
    """
    
    def __init__(self, env: simpy.Environment, spec: ResourceSpec):
        super().__init__(env, spec)
        self.processing_time_factor = 1.0  # baseline
        self.reliability = spec.availability * 0.85  # less reliable (breaks, fatigue)
        self.fatigue_level = 0.0  # 0-1, increases with work
        self.breaks_taken = 0
        
    def get_processing_time(self, task_weight: float) -> float:
        """Calculate processing time for task (with variability and fatigue)"""
        import random
        base_time = 60 / self.spec.speed  # minutes
        # Add human variability (±20%)
        variability = random.uniform(0.8, 1.2)
        # Fatigue effect
        fatigue_effect = 1.0 + (self.fatigue_level * 0.3)  # 30% slower when fully fatigued
        return base_time * self.processing_time_factor * variability * fatigue_effect
    
    def is_available(self) -> bool:
        """Check if resource is available (includes break time)"""
        import random
        # Random breaks every ~2 hours
        if random.random() < 0.01:  # ~1% chance per call
            self.breaks_taken += 1
            return False
        return random.random() < self.reliability
    
    def update_fatigue(self, time_worked: float):
        """Update fatigue level based on work duration"""
        self.fatigue_level = min(1.0, self.fatigue_level + (time_worked / 480))  # 8-hour shift


class ResourcePool:
    """Collection of heterogeneous resources"""
    
    def __init__(self):
        self.resources = []
        self.resource_map = {}  # id -> resource
        
    def add_resource(self, resource: Resource):
        """Add resource to pool"""
        self.resources.append(resource)
        self.resource_map[resource.spec.resource_id] = resource
        
    def get_resource(self, resource_id: str) -> Optional[Resource]:
        """Get resource by ID"""
        return self.resource_map.get(resource_id)
    
    def get_least_busy(self) -> Resource:
        """Get resource with smallest queue"""
        return min(self.resources, key=lambda r: r.get_queue_length())
    
    def get_fastest_available(self) -> Resource:
        """Get fastest available resource"""
        return max(self.resources, key=lambda r: r.spec.speed)
    
    def get_pool_stats(self) -> dict:
        """Get aggregate statistics for entire pool"""
        return {
            'total_resources': len(self.resources),
            'avg_utilization': sum(r.get_utilization() for r in self.resources) / len(self.resources),
            'total_queue_length': sum(r.get_queue_length() for r in self.resources),
            'total_completed': sum(r.num_completed for r in self.resources),
            'total_failed': sum(r.num_failed for r in self.resources),
        }
