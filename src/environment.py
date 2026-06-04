"""
Main Intralogistics Environment: Coordinates Simulation
"""

import simpy
from typing import List, Dict, Optional
import numpy as np
from .resources import (
    Resource, ResourcePool, ResourceSpec,
    AutomatedResource, SemiAutomatedResource, ManualResource
)
from .flow_generator import TaskGenerator, FlowSimulator, Task
from .dispatcher import Dispatcher, create_dispatcher
from .metrics import MetricsCollector


class IntralogisticsEnvironment:
    """Main simulation environment managing all components"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.env = simpy.Environment()
        
        # Initialize components
        self.resource_pool = ResourcePool()
        self.task_generator = TaskGenerator(self.env, config)
        self.flow_simulator = None
        self.dispatcher = None
        self.metrics_collector = MetricsCollector()
        
        # Tracking
        self.active_tasks = []
        self.completed_tasks = []
        self.simulation_time = 0
        self.policy_name = config.get('policy', 'fifo')
        
    def setup_resources(self):
        """Initialize heterogeneous resource fleet"""
        resources_config = self.config.get('resources', [])
        
        if not resources_config:
            # Default configuration if not provided
            resources_config = [
                {
                    'resource_id': 'AGV_1',
                    'type': 'automated',
                    'speed': 20,  # tasks/hour
                    'capacity': 10,
                    'availability': 0.95,
                    'cost_per_hour': 50,
                    'max_payload': 30,
                },
                {
                    'resource_id': 'CONV_1',
                    'type': 'semi_automated',
                    'speed': 15,
                    'capacity': 20,
                    'availability': 0.92,
                    'cost_per_hour': 30,
                    'max_payload': 50,
                },
                {
                    'resource_id': 'OP_1',
                    'type': 'manual',
                    'speed': 10,
                    'capacity': 5,
                    'availability': 0.88,
                    'cost_per_hour': 25,
                    'max_payload': 25,
                },
            ]
        
        for res_config in resources_config:
            spec = ResourceSpec(
                resource_id=res_config['resource_id'],
                resource_type=res_config['type'],
                speed=res_config['speed'],
                capacity=res_config['capacity'],
                availability=res_config['availability'],
                cost_per_hour=res_config['cost_per_hour'],
                max_payload=res_config['max_payload'],
            )
            
            # Create appropriate resource type
            if res_config['type'] == 'automated':
                resource = AutomatedResource(self.env, spec)
            elif res_config['type'] == 'semi_automated':
                resource = SemiAutomatedResource(self.env, spec)
            else:  # manual
                resource = ManualResource(self.env, spec)
            
            self.resource_pool.add_resource(resource)
    
    def setup_dispatcher(self):
        """Initialize dispatcher with specified policy"""
        self.dispatcher = create_dispatcher(self.policy_name, self.resource_pool)
    
    def setup_flow_generation(self):
        """Initialize task generation process"""
        self.flow_simulator = FlowSimulator(self.env, self.task_generator)
    
    def process_task(self, task: Task):
        """Process a task through the system"""
        # Assign to resource
        resource = self.dispatcher.assign_task(task)
        
        # Get processing time based on resource type
        processing_time = resource.get_processing_time(task.weight)
        
        # Simulate processing
        with resource.resource.request() as req:
            yield req
            
            task.start_time = self.env.now
            resource.in_service.append(task)
            resource.busy_time += processing_time
            
            yield self.env.timeout(processing_time)
            
            task.completion_time = self.env.now
            resource.num_completed += 1
            resource.in_service.remove(task)
            
            # Record metrics
            self.metrics_collector.record_task_completion(task)
            self.completed_tasks.append(task)
        
        # Update fatigue for manual resources
        if isinstance(resource, ManualResource):
            resource.update_fatigue(processing_time)
    
    def task_dispatcher_process(self):
        """Main process that dispatches generated tasks to resources"""
        # Wait for tasks to be generated
        while True:
            if self.flow_simulator.get_generated_tasks():
                generated = self.flow_simulator.get_generated_tasks()
                
                # Process all tasks that have been generated but not yet assigned
                for task in generated:
                    if task not in self.active_tasks:
                        self.active_tasks.append(task)
                        self.env.process(self.process_task(task))
            
            yield self.env.timeout(1)  # Check every time unit
    
    def monitoring_process(self):
        """Monitor system state and collect samples"""
        while True:
            # Sample queue length
            total_queue = self.resource_pool.get_pool_stats()['total_queue_length']
            self.metrics_collector.record_queue_sample(total_queue, self.env.now)
            
            # Sample utilization
            avg_util = self.resource_pool.get_pool_stats()['avg_utilization']
            self.metrics_collector.record_utilization_sample(avg_util, self.env.now)
            
            yield self.env.timeout(5)  # Sample every 5 time units
    
    def run(self, until: float = 480):
        """Run the simulation
        
        Args:
            until: Simulation duration in minutes (default: 8 hours = 480 min)
        """
        # Setup all components
        self.setup_resources()
        self.setup_dispatcher()
        self.setup_flow_generation()
        
        # Start monitoring processes
        self.env.process(self.task_dispatcher_process())
        self.env.process(self.monitoring_process())
        
        # Run simulation
        self.env.run(until=until)
        
        self.simulation_time = until
        
        return self.metrics_collector
    
    def get_results(self) -> Dict:
        """Get simulation results"""
        metrics = self.metrics_collector.calculate_metrics()
        
        return {
            'policy': self.policy_name,
            'simulation_time': self.simulation_time,
            'metrics': self.metrics_collector.to_dict(),
            'completed_tasks': len(self.completed_tasks),
            'resource_stats': self.resource_pool.get_pool_stats(),
        }
    
    def print_summary(self):
        """Print simulation summary"""
        print(self.metrics_collector.generate_report())
    
    def export_results(self, filename: str):
        """Export results to CSV"""
        import csv
        
        results = self.get_results()
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['Metric', 'Value'])
            
            # Metrics
            for key, value in results['metrics'].items():
                writer.writerow([key, value])
    
    def export_tasks(self, filename: str):
        """Export completed tasks to CSV"""
        import csv
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'task_id', 'task_type', 'flow_type', 'priority',
                'arrival_time', 'start_time', 'completion_time',
                'due_time', 'lateness', 'on_time', 'assigned_resource'
            ])
            
            # Tasks
            for task in self.completed_tasks:
                writer.writerow([
                    task.task_id,
                    task.task_type,
                    task.flow_type.value,
                    task.priority.name,
                    task.arrival_time,
                    task.start_time,
                    task.completion_time,
                    task.due_time,
                    task.get_lateness(),
                    task.is_on_time(),
                    task.assigned_resource,
                ])
