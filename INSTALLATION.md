# INSTALLATION & SETUP GUIDE

## Quick Start (5 minutes)

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Navigate to project folder:**
```bash
cd intralogistics_simulator
```

2. **Create virtual environment (recommended):**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Verify installation:**
```bash
python -c "import simpy; print('SimPy version:', simpy.__version__)"
```

5. **Run quick test:**
```bash
python main.py test
```

---

## Running Simulations

### Quick Test (Single Scenario)
```bash
python main.py test
```
- Runs one scenario with one policy
- Completes in ~2-5 minutes
- Good for verification

### Full Comparison Study
```bash
python main.py comparison
```
- Tests all 5 scenarios with 4 policies
- ~20 simulation runs total
- Completes in ~30-45 minutes
- Generates comprehensive comparison

### Custom Simulation
```python
from src.environment import IntralogisticsEnvironment
from src.flow_generator import ScenarioBuilder

# Create scenario
scenario = ScenarioBuilder.mixed_flows_scenario(exceptional_ratio=0.20)

# Configure
config = {
    **scenario,
    'policy': 'preemptive'
}

# Run
env = IntralogisticsEnvironment(config)
metrics = env.run(until=480)
env.print_summary()
```

---

## Project Structure

```
intralogistics_simulator/
├── main.py                    # Entry point - RUN THIS
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview
│
├── src/                       # Python source code
│   ├── __init__.py
│   ├── environment.py         # Main simulation loop
│   ├── resources.py           # Resource models
│   ├── flow_generator.py      # Task generation
│   ├── dispatcher.py          # Dispatching policies
│   └── metrics.py             # Performance tracking
│
├── data/                      # Configuration & sample data
│   ├── config.yaml            # Simulation parameters
│   └── sample_tasks.csv       # Example task data
│
├── docs/                      # Documentation
│   ├── PROJECT_PROPOSAL.md    # Research objectives
│   ├── METHODOLOGY.md         # Detailed methodology
│   └── RESULTS_TEMPLATE.md    # Report template
│
└── results/                   # Output directory (auto-created)
    ├── tasks_*.csv            # Detailed task records
    ├── results_*.csv          # Performance metrics
    └── comparison_*.json      # Comparison summaries
```

---

## Configuration

### Main Parameters in config.yaml

```yaml
# Flow generation
flows:
  nominal_rate: 10           # tasks per hour
  exceptional_ratio: 0.15    # fraction of workload

# Dispatching policy
dispatcher:
  policy: "priority"         # fifo|priority|load_balancing|preemptive|adaptive

# Resources (configure your fleet)
resources:
  - resource_id: "AGV_1"
    type: "automated"
    speed: 20                # tasks/hour
    availability: 0.95       # uptime fraction
    # ... more params
```

### Policy Options

| Policy | Best For | Trade-offs |
|--------|----------|-----------|
| **FIFO** | Baseline comparison | Fair but not optimized |
| **Priority** | Mixed nominal+exceptional | Nominal tasks wait |
| **Load-Balancing** | Smooth demand | No differentiation |
| **Preemptive** | Critical exceptions | Risk of starvation |
| **Adaptive** | Variable conditions | More complex |

---

## Output Files

After running a simulation, check `results/` folder:

### CSV Files
```
tasks_[scenario]_[policy]_[timestamp].csv
- One row per completed task
- Columns: task_id, flow_type, arrival_time, completion_time, lateness, etc.
- Use for detailed analysis

results_[scenario]_[policy]_[timestamp].csv
- One row of aggregate metrics
- Columns: completed_tasks, on_time_tasks, service_level, avg_lateness, etc.
- Use for quick comparison
```

### JSON Files
```
comparison_summary_[timestamp].json
- All scenarios × all policies
- Hierarchical structure for easy analysis
- Good for programmatic processing
```

---

## Analysis & Visualization

### View Results
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load task data
tasks = pd.read_csv('results/tasks_*.csv')

# Plot lateness distribution
plt.hist(tasks['lateness'], bins=30)
plt.xlabel('Lateness (minutes)')
plt.ylabel('Frequency')
plt.show()

# Compare policies
results = pd.read_csv('results/results_*.csv')
print(results[['policy', 'service_level', 'avg_lateness']])
```

### Key Metrics to Compare
1. **Service Level %**: On-time delivery rate
2. **Avg Lateness**: Average task lateness (minutes)
3. **Max Lateness**: Worst-case lateness
4. **Avg Queue**: Resource congestion
5. **Utilization**: Resource efficiency
6. **Robustness Index**: Consistency measure

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'simpy'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Simulation runs very slowly
**Solution:** 
- Reduce simulation duration in main.py
- Use fewer replications
- Check if processes are creating too many events

### Issue: Results folder not created
**Solution:** It's auto-created on first run. If not:
```bash
mkdir results
```

### Issue: Random seed for reproducibility
**Solution:** Set seed in environment:
```python
import random, numpy as np
random.seed(42)
np.random.seed(42)
```

---

## Performance Tips

### Faster Runs
```python
# Reduce simulation time
env.run(until=240)  # 4 hours instead of 8

# Reduce task volume
config['nominal_rate'] = 5  # instead of 10

# Fewer replications for quick tests
```

### Memory Efficiency
```python
# Don't store all task details
collector.completed_tasks = []  # Clear periodically

# Use generators instead of lists
# Process results on-the-fly
```

### Parallel Runs
```bash
# Run multiple scenarios in parallel (Unix/Mac)
(python main.py test &) && (python main.py test &)

# Or use Python multiprocessing
from multiprocessing import Pool
```

---

## Advanced Usage

### Custom Resource Type
```python
from src.resources import Resource, ResourceSpec

class SpecializedResource(Resource):
    def get_processing_time(self, task_weight):
        # Custom logic
        return special_calculation(task_weight)
```

### Custom Dispatching Policy
```python
from src.dispatcher import DispatchPolicy

class MyPolicy(DispatchPolicy):
    def select_resource(self, task, pool):
        # Custom selection logic
        return best_resource
```

### Batch Analysis
```python
from src.environment import IntralogisticsEnvironment
from src.flow_generator import ScenarioBuilder

for ratio in [0.10, 0.15, 0.20, 0.30]:
    scenario = ScenarioBuilder.mixed_flows_scenario(ratio)
    env = IntralogisticsEnvironment({**scenario, 'policy': 'priority'})
    env.run()
    env.export_results(f'results/sensitivity_{ratio}.csv')
```

---

## Support & References

- **SimPy Documentation**: https://simpy.readthedocs.io/
- **Project Files**: See docs/ folder
- **Issues/Questions**: Check README.md and PROJECT_PROPOSAL.md

---

## Next Steps

1. ✓ Install & verify (main.py test)
2. ✓ Understand methodology (read METHODOLOGY.md)
3. ✓ Run full comparison (main.py comparison)
4. ✓ Analyze results (use provided templates)
5. ✓ Modify & extend (customize config.yaml)

---

**Version**: 0.1.0  
**Last Updated**: 2026-06-04
