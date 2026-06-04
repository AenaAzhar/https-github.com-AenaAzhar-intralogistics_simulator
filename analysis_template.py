"""
Analysis Notebook Template
Use this as a starting point for Jupyter notebook analysis
"""

# !pip install jupyter pandas matplotlib seaborn

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)

# ============================================================================
# 1. LOAD SIMULATION RESULTS
# ============================================================================

results_dir = Path('results')

# Find latest result files
task_files = sorted(results_dir.glob('tasks_*.csv'))
result_files = sorted(results_dir.glob('results_*.csv'))

if task_files:
    latest_task_file = task_files[-1]
    tasks = pd.read_csv(latest_task_file)
    print(f"Loaded tasks from: {latest_task_file}")
    print(f"Total tasks: {len(tasks)}")
    print(tasks.head())
else:
    print("No task files found. Run simulation first: python main.py comparison")

# ============================================================================
# 2. BASIC STATISTICS
# ============================================================================

print("\n=== PERFORMANCE SUMMARY ===")
print(f"On-time delivery: {(tasks['on_time'].sum() / len(tasks) * 100):.1f}%")
print(f"Average lateness: {tasks['lateness'].mean():.2f} minutes")
print(f"Maximum lateness: {tasks['lateness'].max():.2f} minutes")

# By flow type
for flow_type in tasks['flow_type'].unique():
    flow_tasks = tasks[tasks['flow_type'] == flow_type]
    on_time_pct = (flow_tasks['on_time'].sum() / len(flow_tasks) * 100)
    avg_lateness = flow_tasks['lateness'].mean()
    print(f"\n{flow_type.upper()}:")
    print(f"  Tasks: {len(flow_tasks)}")
    print(f"  On-time: {on_time_pct:.1f}%")
    print(f"  Avg lateness: {avg_lateness:.2f} min")

# ============================================================================
# 3. VISUALIZATIONS
# ============================================================================

# 3.1 Lateness Distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(tasks['lateness'], bins=30, edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Lateness (minutes)')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Lateness Distribution')
axes[0].axvline(tasks['lateness'].mean(), color='red', linestyle='--', label='Mean')
axes[0].legend()

# 3.2 On-time by flow type
flow_data = tasks.groupby('flow_type').agg({
    'on_time': 'sum',
    'task_id': 'count'
})
flow_data['on_time_pct'] = (flow_data['on_time'] / flow_data['task_id'] * 100)

axes[1].bar(flow_data.index, flow_data['on_time_pct'], color=['steelblue', 'coral'])
axes[1].set_ylabel('On-time Delivery %')
axes[1].set_title('Service Level by Flow Type')
axes[1].set_ylim(0, 105)
for i, v in enumerate(flow_data['on_time_pct']):
    axes[1].text(i, v + 2, f'{v:.1f}%', ha='center')

plt.tight_layout()
plt.show()

# 3.3 Lateness by resource (if available)
if 'assigned_resource' in tasks.columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    resource_data = tasks.groupby('assigned_resource')['lateness'].agg(['mean', 'std', 'count'])
    resource_data['mean'].plot(kind='bar', ax=ax, yerr=resource_data['std'], capsize=4)
    ax.set_ylabel('Average Lateness (minutes)')
    ax.set_xlabel('Resource')
    ax.set_title('Average Task Lateness by Resource')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ============================================================================
# 4. POLICY COMPARISON
# ============================================================================

if result_files:
    print("\n=== POLICY COMPARISON ===")
    
    all_results = []
    for result_file in result_files[-5:]:  # Last 5 runs
        try:
            df = pd.read_csv(result_file)
            all_results.append(df)
        except:
            pass
    
    if all_results:
        comparison = pd.concat(all_results, ignore_index=True)
        
        # Summary by policy
        if 'policy' in comparison.columns:
            policy_summary = comparison.groupby('policy').agg({
                'completed_tasks': 'mean',
                'on_time_tasks': 'mean',
                'avg_lateness': 'mean',
                'robustness_index': 'mean'
            })
            
            print(policy_summary.round(2))
            
            # Visualize
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            
            for idx, metric in enumerate(['on_time_tasks', 'avg_lateness', 'robustness_index', 'avg_queue_length']):
                if metric in comparison.columns:
                    ax = axes[idx // 2, idx % 2]
                    comparison.groupby('policy')[metric].mean().plot(kind='bar', ax=ax, color='steelblue')
                    ax.set_title(f'Comparison: {metric}')
                    ax.set_ylabel(metric)
                    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            
            plt.tight_layout()
            plt.show()

# ============================================================================
# 5. SENSITIVITY ANALYSIS
# ============================================================================

# Analyze impact of flow type on performance
print("\n=== SENSITIVITY ANALYSIS ===")

# Exception ratio effect
exception_counts = tasks.groupby('flow_type').size()
if len(exception_counts) > 1:
    total = exception_counts.sum()
    exception_ratio = exception_counts.get('exceptional', 0) / total
    print(f"Exceptional flow ratio: {exception_ratio:.1%}")
    
    # Compare performance
    exceptional_perf = tasks[tasks['flow_type'] == 'exceptional']
    nominal_perf = tasks[tasks['flow_type'] == 'nominal']
    
    if len(exceptional_perf) > 0 and len(nominal_perf) > 0:
        print(f"Nominal avg lateness: {nominal_perf['lateness'].mean():.2f} min")
        print(f"Exceptional avg lateness: {exceptional_perf['lateness'].mean():.2f} min")
        print(f"Impact: {exceptional_perf['lateness'].mean() - nominal_perf['lateness'].mean():.2f} min")

# ============================================================================
# 6. TIME-SERIES ANALYSIS
# ============================================================================

if 'completion_time' in tasks.columns:
    # Sort by completion time
    tasks_sorted = tasks.sort_values('completion_time')
    
    # Calculate cumulative on-time
    tasks_sorted['cumulative_on_time'] = tasks_sorted['on_time'].cumsum()
    tasks_sorted['cumulative_total'] = range(1, len(tasks_sorted) + 1)
    tasks_sorted['service_level'] = (tasks_sorted['cumulative_on_time'] / 
                                      tasks_sorted['cumulative_total'] * 100)
    
    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(tasks_sorted['completion_time'], tasks_sorted['service_level'], 
            marker='o', markersize=3, linewidth=1.5, alpha=0.7)
    ax.set_xlabel('Completion Time (minutes)')
    ax.set_ylabel('Service Level (%)')
    ax.set_title('Service Level Evolution Over Time')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 105)
    plt.tight_layout()
    plt.show()

print("\n=== ANALYSIS COMPLETE ===")
