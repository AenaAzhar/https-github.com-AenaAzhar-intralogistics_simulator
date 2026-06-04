"""
Flow Generator: Models Nominal and Exceptional Intralogistics Flows
"""

import simpy
from dataclasses import dataclass
from enum import Enum
from typing import List, Callable
import random
import numpy as np
from datetime import datetime


class FlowType(Enum):
    """Classification of intralogistics flows"""
    NOMINAL = "nominal"
    EXCEPTIONAL = "exceptional"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 3
    NORMAL = 2
    HIGH = 1
    URGENT = 0


@dataclass
class Task:
    """Represents a logistics task (pick, kit, deliver, return)"""
    task_id: int
    task_type: str  # 'pick', 'kit', 'deliver', 'return'
    flow_type: FlowType  # nominal or exceptional
    priority: TaskPriority
    arrival_time: float  # SimPy environment time
    due_time: float  # deadline for completion
    weight: float  # kg, affects processing time
    origin: str  # 'warehouse', 'supermarket', etc.
    destination: str  # 'line', 'supermarket', etc.
    
    # Tracking fields
    start_time: float = None
    completion_time: float = None
    assigned_resource: str = None
    
    def get_lateness(self) -> float:
        """Calculate lateness (negative = early, positive = late)"""
        if self.completion_time is None:
            return 0
        return max(0, self.completion_time - self.due_time)
    
    def is_on_time(self) -> bool:
        """Check if task completed on time"""
        if self.completion_time is None:
            return False
        return self.completion_time <= self.due_time


class TaskGenerator:
    """Generates nominal and exceptional tasks"""
    
    def __init__(self, env: simpy.Environment, config: dict):
        self.env = env
        self.config = config
        self.task_counter = 0
        self.nominal_arrival_rate = config.get('nominal_rate', 10)  # tasks/hour
        self.exceptional_ratio = config.get('exceptional_ratio', 0.15)  # % of workload
        if self.exceptional_ratio >= 1:
            raise ValueError("exceptional_ratio must be less than 1.0")
        self.exceptional_arrival_rate = (
            (self.nominal_arrival_rate * self.exceptional_ratio) / (1 - self.exceptional_ratio)
            if self.exceptional_ratio > 0
            else 0
        )
        
    def generate_nominal_task(self) -> Task:
        """Generate a nominal task (scheduled production)"""
        self.task_counter += 1
        
        # Nominal tasks are fairly predictable
        weight = np.random.normal(loc=10, scale=2)  # kg
        weight = max(1, min(20, weight))  # clamp between 1-20 kg
        
        # Due time: 30-120 minutes from now
        due_in = random.uniform(30, 120)
        
        task = Task(
            task_id=self.task_counter,
            task_type=random.choice(['pick', 'kit', 'deliver']),
            flow_type=FlowType.NOMINAL,
            priority=TaskPriority.NORMAL,
            arrival_time=self.env.now,
            due_time=self.env.now + due_in,
            weight=weight,
            origin=random.choice(['warehouse', 'supermarket']),
            destination='line'
        )
        return task
    
    def generate_exceptional_task(self) -> Task:
        """Generate an exceptional task (urgent, unplanned)"""
        self.task_counter += 1
        
        # Exceptional tasks: varied characteristics
        weight = np.random.normal(loc=12, scale=3)  # higher variance, slightly heavier
        weight = max(1, min(25, weight))
        
        # Due time: 5-30 minutes from now (urgent!)
        due_in = random.uniform(5, 30)
        
        task = Task(
            task_id=self.task_counter,
            task_type=random.choice(['pick', 'return', 'rework']),
            flow_type=FlowType.EXCEPTIONAL,
            priority=random.choice([TaskPriority.HIGH, TaskPriority.URGENT]),
            arrival_time=self.env.now,
            due_time=self.env.now + due_in,
            weight=weight,
            origin=random.choice(['warehouse', 'supermarket', 'line']),
            destination=random.choice(['line', 'warehouse', 'supermarket'])
        )
        return task
    
    def generate_task(self) -> Task:
        """Generate either nominal or exceptional task based on ratio"""
        if random.random() < self.exceptional_ratio:
            return self.generate_exceptional_task()
        else:
            return self.generate_nominal_task()


class FlowSimulator:
    """Manages task generation and arrival process"""
    
    def __init__(self, env: simpy.Environment, generator: TaskGenerator):
        self.env = env
        self.generator = generator
        self.tasks_generated = []
        self.action = env.process(self.run())
    
    def run(self):
        """Main task generation loop"""
        while True:
            # Generate interval (Poisson process)
            interval = np.random.exponential(scale=60 / self.generator.nominal_arrival_rate)
            yield self.env.timeout(interval)
            
            task = self.generator.generate_task()
            self.tasks_generated.append(task)
    
    def get_generated_tasks(self) -> List[Task]:
        """Get all generated tasks"""
        return self.tasks_generated
    
    def get_summary(self) -> dict:
        """Get summary statistics"""
        nominal_count = sum(1 for t in self.tasks_generated if t.flow_type == FlowType.NOMINAL)
        exceptional_count = sum(1 for t in self.tasks_generated if t.flow_type == FlowType.EXCEPTIONAL)
        
        return {
            'total_tasks': len(self.tasks_generated),
            'nominal_tasks': nominal_count,
            'exceptional_tasks': exceptional_count,
            'exceptional_ratio': exceptional_count / len(self.tasks_generated) if self.tasks_generated else 0,
        }


class ScenarioBuilder:
    """Build different simulation scenarios"""
    
    @staticmethod
    def baseline_scenario() -> dict:
        """Baseline: Nominal flows only"""
        return {
            'name': 'Baseline - Nominal Only',
            'nominal_rate': 10,  # tasks/hour
            'exceptional_ratio': 0.0,
            'resource_availability': 1.0,
            'demand_multiplier': 1.0,
        }
    
    @staticmethod
    def mixed_flows_scenario(exceptional_ratio=0.15) -> dict:
        """Mixed flows: Nominal + Exceptional"""
        return {
            'name': f'Mixed Flows - {exceptional_ratio*100}% Exceptional',
            'nominal_rate': 10,
            'exceptional_ratio': exceptional_ratio,
            'resource_availability': 1.0,
            'demand_multiplier': 1.0,
        }
    
    @staticmethod
    def resource_unavailability_scenario(unavailable_percent=0.1) -> dict:
        """Resource unavailability: One resource fails"""
        return {
            'name': f'Resource Unavailable - {unavailable_percent*100}% Down',
            'nominal_rate': 10,
            'exceptional_ratio': 0.15,
            'resource_availability': 1.0 - unavailable_percent,
            'demand_multiplier': 1.0,
        }
    
    @staticmethod
    def demand_spike_scenario(multiplier=1.5) -> dict:
        """Demand spike: Increased workload"""
        return {
            'name': f'Demand Spike - {multiplier}x Normal',
            'nominal_rate': 10 * multiplier,
            'exceptional_ratio': 0.15,
            'resource_availability': 1.0,
            'demand_multiplier': multiplier,
        }
