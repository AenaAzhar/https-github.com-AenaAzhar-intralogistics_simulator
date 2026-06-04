# QUICK RUNNING GUIDE

## 30-Second Start

```bash
# 1. Open terminal in project folder
cd "c:\Users\A\Desktop\reserch paper work\fleet managment\intralogistics_simulator"

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Run quick test
python main.py test
```

Expected output: Simulation results summary with performance metrics.

---

## What Each Command Does

### Test Mode (Recommended First)
```bash
python main.py test
```
- **Time**: ~2-5 minutes
- **What**: Runs 1 scenario (mixed flows) with 1 policy (priority)
- **Output**: Performance metrics, CSV files
- **Best for**: Verification, quick check

### Comparison Mode (Full Study)
```bash
python main.py comparison
```
- **Time**: ~30-45 minutes
- **What**: Runs 5 scenarios × 4 policies = 20 simulation runs
- **Output**: All metrics, comparison summary in JSON
- **Best for**: Comprehensive analysis, policy selection

### Help
```bash
python main.py help
```
- Display this guide and usage information

---

## Interpreting Results

After running, check the `results/` folder for:

### CSV Files
- `tasks_*.csv` - Detailed task data
- `results_*.csv` - Aggregated metrics

### Key Metrics to Look For

| Metric | Good Value | What It Means |
|--------|-----------|--------------|
| **Service Level** | > 95% | % of on-time deliveries |
| **Avg Lateness** | < 10 min | Average delay in minutes |
| **Max Lateness** | < 60 min | Worst-case delay |
| **Avg Queue** | 2-4 tasks | Resource congestion level |
| **Utilization** | 75-85% | Resource efficiency |
| **Robustness** | > 0.7 | Consistency of performance |

---

## File Overview

```
Project Root Files:
├── main.py              ← RUN THIS
├── requirements.txt     ← Dependencies (pip install -r)
├── README.md            ← Project overview
├── INSTALLATION.md      ← Setup instructions
└── RUNNING_GUIDE.md     ← This file

Documentation:
├── docs/PROJECT_PROPOSAL.md     ← Research objectives
├── docs/METHODOLOGY.md           ← How it works (detailed)
└── docs/RESULTS_TEMPLATE.md      ← How to report findings

Source Code:
├── src/environment.py    ← Main simulation
├── src/resources.py      ← Fleet models
├── src/flow_generator.py ← Task generation
├── src/dispatcher.py     ← Dispatching policies
└── src/metrics.py        ← Performance tracking

Analysis:
└── analysis_template.py  ← For Jupyter/Python analysis

Configuration:
└── data/config.yaml      ← Simulation parameters
```

---

## Customization Examples

### Change Policy
Edit `main.py` → Change `policy = 'priority'` to:
- `'fifo'` - Simple first-come-first-served
- `'load_balancing'` - Balance resources
- `'preemptive'` - Urgent tasks can interrupt

### Change Scenario
In `main.py`, modify:
```python
scenario = ScenarioBuilder.mixed_flows_scenario(exceptional_ratio=0.30)
```

### Change Resource Fleet
Edit `data/config.yaml` → Modify resources section:
```yaml
resources:
  - resource_id: "AGV_1"
    speed: 20  # faster/slower
    availability: 0.95  # more/less reliable
```

---

## Troubleshooting

**Q: "Module not found: simpy"**  
A: Run: `pip install -r requirements.txt`

**Q: Simulation is slow**  
A: Reduce duration or check config.yaml

**Q: No results folder**  
A: It's auto-created on first run. Check the console output.

**Q: Want reproducible results**  
A: The simulation uses random seeds for variability (realistic). Use same scenario/policy for similar results.

---

## Next Steps

1. ✓ Run `python main.py test` to verify it works
2. ✓ Check the `results/` folder for output files
3. ✓ Read `docs/METHODOLOGY.md` to understand what's happening
4. ✓ Run `python main.py comparison` for full analysis
5. ✓ Customize configuration and run your own scenarios

---

## Output Examples

### Sample Console Output
```
======================================================================
Run 1: Mixed Flows - 15% Exceptional + PRIORITY Policy
======================================================================

╔══════════════════════════════════════════════════════════╗
║        INTRALOGISTICS SIMULATION RESULTS REPORT         ║
╚══════════════════════════════════════════════════════════╝

TASK PERFORMANCE:
  • Total Completed:      487
  • On-Time Tasks:        462 (94.9%)
  • Late Tasks:           25
  
LATENESS ANALYSIS:
  • Average Lateness:     4.32 min
  • Maximum Lateness:     41.23 min

RESOURCE UTILIZATION:
  • Average:              81.2%
  • Average Queue Length: 2.45 tasks

RESILIENCE:
  • Robustness Index:     0.87/1.00
```

### CSV Output (results_*.csv)
```
completed_tasks,on_time_tasks,service_level,avg_lateness,...
487,462,94.9,4.32,...
```

---

## Academic Use

This project demonstrates:
- ✓ Discrete-Event Simulation (SimPy)
- ✓ Heterogeneous Resource Management
- ✓ Dispatching Policies & Optimization
- ✓ Performance Analysis & Metrics
- ✓ Scenario-Based Experimentation
- ✓ Resilience Engineering

Perfect for:
- PhD thesis foundation
- Conference paper results
- Course projects
- Industrial case studies

---

**Version**: 0.1.0  
**Last Updated**: 2026-06-04
