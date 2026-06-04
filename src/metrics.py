"""
Metrics Collection and KPI Tracking
"""

from typing import List, Dict
from dataclasses import dataclass, field
import numpy as np
from .flow_generator import Task, FlowType


@dataclass
class SimulationMetrics:
    """Container for simulation performance metrics"""
    
    # Service metrics
    completed_tasks: int = 0
    on_time_tasks: int = 0
    late_tasks: int = 0
    avg_lateness: float = 0.0
    max_lateness: float = 0.0
    service_level: float = 0.0  # % on-time delivery
    
    # Flow-specific metrics
    nominal_on_time: int = 0
    nominal_total: int = 0
    exceptional_on_time: int = 0
    exceptional_total: int = 0
    
    # Resource metrics
    avg_utilization: float = 0.0
    max_queue_length: int = 0
    avg_queue_length: float = 0.0
    
    # Exceptional flow impact
    exceptional_avg_lateness: float = 0.0
    nominal_avg_lateness: float = 0.0
    exceptional_impact: float = 0.0  # additional lateness caused by exceptions
    
    # Resilience metrics
    variance_completion_time: float = 0.0
    robustness_index: float = 0.0  # 0-1, higher is better
    
    # Advanced metrics
    task_lateness_list: List[float] = field(default_factory=list)
    queue_length_history: List[int] = field(default_factory=list)
    utilization_history: List[float] = field(default_factory=list)


class MetricsCollector:
    """Collects and aggregates performance metrics during simulation"""
    
    def __init__(self):
        self.completed_tasks: List[Task] = []
        self.queue_length_samples: List[int] = []
        self.utilization_samples: List[float] = []
        self.sample_times: List[float] = []
    
    def record_task_completion(self, task: Task):
        """Record task completion"""
        self.completed_tasks.append(task)
    
    def record_queue_sample(self, queue_length: int, time: float):
        """Record queue length sample"""
        self.queue_length_samples.append(queue_length)
        self.sample_times.append(time)
    
    def record_utilization_sample(self, utilization: float, time: float):
        """Record resource utilization sample"""
        self.utilization_samples.append(utilization)
    
    def calculate_metrics(self) -> SimulationMetrics:
        """Calculate all performance metrics"""
        metrics = SimulationMetrics()
        
        if not self.completed_tasks:
            return metrics
        
        # Basic counts
        metrics.completed_tasks = len(self.completed_tasks)
        
        # Lateness calculations
        lateness_list = [task.get_lateness() for task in self.completed_tasks]
        on_time = sum(1 for task in self.completed_tasks if task.is_on_time())
        
        metrics.on_time_tasks = on_time
        metrics.late_tasks = metrics.completed_tasks - on_time
        metrics.service_level = (on_time / metrics.completed_tasks * 100) if metrics.completed_tasks > 0 else 0
        metrics.avg_lateness = np.mean(lateness_list) if lateness_list else 0
        metrics.max_lateness = np.max(lateness_list) if lateness_list else 0
        metrics.task_lateness_list = lateness_list
        
        # Flow-specific metrics
        nominal_tasks = [t for t in self.completed_tasks if t.flow_type == FlowType.NOMINAL]
        exceptional_tasks = [t for t in self.completed_tasks if t.flow_type == FlowType.EXCEPTIONAL]
        
        metrics.nominal_total = len(nominal_tasks)
        metrics.exceptional_total = len(exceptional_tasks)
        
        if nominal_tasks:
            metrics.nominal_on_time = sum(1 for t in nominal_tasks if t.is_on_time())
            metrics.nominal_avg_lateness = np.mean([t.get_lateness() for t in nominal_tasks])
        
        if exceptional_tasks:
            metrics.exceptional_on_time = sum(1 for t in exceptional_tasks if t.is_on_time())
            metrics.exceptional_avg_lateness = np.mean([t.get_lateness() for t in exceptional_tasks])
        
        # Exceptional flow impact
        if nominal_tasks and exceptional_tasks:
            metrics.exceptional_impact = metrics.exceptional_avg_lateness - metrics.nominal_avg_lateness
        
        # Queue metrics
        if self.queue_length_samples:
            metrics.avg_queue_length = np.mean(self.queue_length_samples)
            metrics.max_queue_length = np.max(self.queue_length_samples)
            metrics.queue_length_history = self.queue_length_samples
        
        # Utilization metrics
        if self.utilization_samples:
            metrics.avg_utilization = np.mean(self.utilization_samples)
            metrics.utilization_history = self.utilization_samples
        
        # Variance in completion times (indicates variability/robustness)
        if lateness_list:
            metrics.variance_completion_time = np.var(lateness_list)
        
        # Robustness index: lower variance + higher service level = more robust
        # Range: 0-1, higher is better
        service_component = metrics.service_level / 100.0
        variance_component = max(0, 1.0 - (metrics.variance_completion_time / 100.0))
        metrics.robustness_index = (service_component + variance_component) / 2.0
        
        return metrics
    
    def generate_report(self) -> str:
        """Generate human-readable performance report"""
        metrics = self.calculate_metrics()
        
        report = f"""
╔══════════════════════════════════════════════════════════╗
║        INTRALOGISTICS SIMULATION RESULTS REPORT         ║
╚══════════════════════════════════════════════════════════╝

TASK PERFORMANCE:
  • Total Completed:      {metrics.completed_tasks}
  • On-Time Tasks:        {metrics.on_time_tasks} ({metrics.service_level:.1f}%)
  • Late Tasks:           {metrics.late_tasks}
  
LATENESS ANALYSIS:
  • Average Lateness:     {metrics.avg_lateness:.2f} min
  • Maximum Lateness:     {metrics.max_lateness:.2f} min
  • Variance:             {metrics.variance_completion_time:.2f}

FLOW-TYPE COMPARISON:
  • Nominal Tasks:        {metrics.nominal_total} ({metrics.nominal_on_time} on-time, {metrics.nominal_avg_lateness:.2f} avg lat.)
  • Exceptional Tasks:    {metrics.exceptional_total} ({metrics.exceptional_on_time} on-time, {metrics.exceptional_avg_lateness:.2f} avg lat.)
  • Exception Impact:     +{metrics.exceptional_impact:.2f} min additional lateness

RESOURCE UTILIZATION:
  • Average:              {metrics.avg_utilization:.1%}
  • Average Queue Length: {metrics.avg_queue_length:.2f} tasks
  • Max Queue Length:     {metrics.max_queue_length} tasks

RESILIENCE:
  • Robustness Index:     {metrics.robustness_index:.2f}/1.00

╚══════════════════════════════════════════════════════════╝
"""
        return report
    
    def to_dict(self) -> dict:
        """Convert metrics to dictionary for export"""
        metrics = self.calculate_metrics()
        
        return {
            'completed_tasks': metrics.completed_tasks,
            'on_time_tasks': metrics.on_time_tasks,
            'service_level': metrics.service_level,
            'avg_lateness': metrics.avg_lateness,
            'max_lateness': metrics.max_lateness,
            'avg_queue_length': metrics.avg_queue_length,
            'max_queue_length': metrics.max_queue_length,
            'avg_utilization': metrics.avg_utilization,
            'robustness_index': metrics.robustness_index,
            'nominal_on_time_pct': (metrics.nominal_on_time / metrics.nominal_total * 100) if metrics.nominal_total > 0 else 0,
            'exceptional_on_time_pct': (metrics.exceptional_on_time / metrics.exceptional_total * 100) if metrics.exceptional_total > 0 else 0,
            'exceptional_avg_lateness': metrics.exceptional_avg_lateness,
            'nominal_avg_lateness': metrics.nominal_avg_lateness,
        }
