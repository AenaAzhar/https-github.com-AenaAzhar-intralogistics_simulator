"""
Main Entry Point: Run Intralogistics Simulation
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.environment import IntralogisticsEnvironment
from src.flow_generator import ScenarioBuilder


def make_json_safe(value):
    """Convert NumPy values to standard Python types for JSON export."""
    if isinstance(value, dict):
        return {key: make_json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [make_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return tuple(make_json_safe(item) for item in value)
    if isinstance(value, np.generic):
        return value.item()
    return value


def run_single_simulation(scenario: dict, policy: str, run_id: int = 1):
    """Run a single simulation with given scenario and policy"""
    
    print(f"\n{'='*70}")
    print(f"Run {run_id}: {scenario['name']} + {policy.upper()} Policy")
    print(f"{'='*70}")
    
    # Create config
    config = {
        **scenario,
        'policy': policy,
    }
    
    # Create and run environment
    env = IntralogisticsEnvironment(config)
    metrics_collector = env.run(until=480)  # 8 hours
    
    # Display results
    env.print_summary()
    
    # Export results
    results_dir = Path('results')
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    scenario_name = scenario['name'].replace(' ', '_').replace('-', '_').lower()
    
    task_file = results_dir / f"tasks_{scenario_name}_{policy}_{timestamp}.csv"
    results_file = results_dir / f"results_{scenario_name}_{policy}_{timestamp}.csv"
    
    env.export_tasks(str(task_file))
    env.export_results(str(results_file))
    
    print(f"\nOK Tasks exported: {task_file}")
    print(f"OK Results exported: {results_file}")
    
    return env.get_results()


def run_comparison_study():
    """Run comprehensive comparison study"""
    
    print("\n" + "="*70)
    print(" INTRALOGISTICS SIMULATOR: COMPREHENSIVE COMPARISON STUDY")
    print("="*70)
    
    # Define scenarios to test
    scenarios = [
        ScenarioBuilder.baseline_scenario(),
        ScenarioBuilder.mixed_flows_scenario(exceptional_ratio=0.15),
        ScenarioBuilder.mixed_flows_scenario(exceptional_ratio=0.30),
        ScenarioBuilder.resource_unavailability_scenario(unavailable_percent=0.10),
        ScenarioBuilder.demand_spike_scenario(multiplier=1.5),
    ]
    
    # Define policies to compare
    policies = [
        'fifo',
        'priority',
        'load_balancing',
        'preemptive',
    ]
    
    # Run all combinations
    all_results = {}
    run_count = 0
    
    for scenario in scenarios:
        scenario_results = {}
        
        for policy in policies:
            run_count += 1
            
            try:
                results = run_single_simulation(scenario, policy, run_count)
                scenario_results[policy] = results['metrics']
                
            except Exception as e:
                print(f"\nERROR in run {run_count}: {e}")
                scenario_results[policy] = None
        
        all_results[scenario['name']] = scenario_results
    
    # Save comprehensive results
    results_dir = Path('results')
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    summary_file = results_dir / f"comparison_summary_{timestamp}.json"
    
    with open(summary_file, 'w') as f:
        json.dump(make_json_safe(all_results), f, indent=2)
    
    print(f"\nOK Comparison summary saved: {summary_file}")
    
    return all_results


def run_quick_test():
    """Quick test with single scenario and policy"""
    
    print("\n" + "="*70)
    print(" INTRALOGISTICS SIMULATOR: QUICK TEST")
    print("="*70)
    
    scenario = ScenarioBuilder.mixed_flows_scenario(exceptional_ratio=0.15)
    policy = 'priority'
    
    results = run_single_simulation(scenario, policy, run_id=1)
    
    return results


def print_help():
    """Print help information"""
    print("""
INTRALOGISTICS SIMULATOR
Heterogeneous Fleet Management for Resilient Intralogistics

Usage:
    python main.py [mode]

Modes:
    test        - Quick test run with default scenario (default)
    comparison  - Full comparison study of all scenarios and policies
    help        - Show this help message

Examples:
    python main.py
    python main.py test
    python main.py comparison
    python main.py help

Output:
    - Console: Simulation progress and results summary
    - CSV Files: Detailed task and metrics data in results/ folder
    - JSON Files: Comparison data for analysis

For more information, see:
    - docs/PROJECT_PROPOSAL.md
    - docs/METHODOLOGY.md
    - README.md
""")


if __name__ == '__main__':
    
    # Get mode from command line
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else 'test'
    
    if mode == 'help':
        print_help()
    
    elif mode == 'comparison':
        all_results = run_comparison_study()
        
        print("\n" + "="*70)
        print(" COMPARISON COMPLETE")
        print("="*70)
        print(f"\nTotal scenarios tested: {len(all_results)}")
        print("Results saved to results/ folder")
    
    else:  # test or default
        results = run_quick_test()
        
        print("\n" + "="*70)
        print(" TEST COMPLETE")
        print("="*70)
        print("\nTo run full comparison study:")
        print("  python main.py comparison")


