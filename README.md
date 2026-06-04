# Mini Intralogistics Simulator: Heterogeneous Fleet Management

## Project Overview

A discrete-event simulation framework for modeling aerospace intralogistics systems with heterogeneous resources under nominal and exceptional production flows.

**Target Application:** Line-side logistics, warehouse-to-line picking, kitting, supermarkets, returns management

## Key Features

- **Nominal Flows**: Standard scheduled production requests
- **Exceptional Flows**: Late replanning, quality events, rework, missing items, returns
- **Heterogeneous Resources**: Automated (AGVs), semi-automated (conveyors), and human operators
- **Dispatching Policies**: Rule-based and priority management
- **Performance Metrics**: Service robustness, capacity utilization, resilience indicators

## Project Structure

```
intralogistics_simulator/
├── src/                          # Source code
│   ├── __init__.py
│   ├── environment.py            # Main simulation environment
│   ├── resources.py              # Heterogeneous fleet models
│   ├── flow_generator.py         # Nominal & exceptional flow generation
│   ├── dispatcher.py             # Dispatching policies
│   └── metrics.py                # Performance KPIs
├── data/                         # Configuration & test data
│   ├── config.yaml               # Simulation parameters
│   ├── nominal_flows.csv         # Historical nominal flow data
│   └── exceptional_flows.csv     # Historical exceptional flow data
├── docs/                         # Documentation
│   ├── PROJECT_PROPOSAL.md       # Full project proposal
│   ├── METHODOLOGY.md            # Research methodology
│   └── RESULTS_TEMPLATE.md       # Results reporting template
├── notebooks/                    # Jupyter notebooks for analysis
├── results/                      # Output & results
├── requirements.txt              # Dependencies
└── main.py                       # Entry point
```

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run Simulation

```bash
python main.py
```

### View Results

Check `results/` folder for generated reports and metrics.

## Research Questions

1. How do nominal and exceptional flows interact in line-side logistics?
2. What dispatching policies minimize shortages and service delays?
3. How much capacity slack is needed for resilience under uncertainty?
4. How do heterogeneous resources compare in handling mixed workloads?

## Expected Outputs

- Discrete-event simulation model
- Comparative analysis of 3-4 dispatching policies
- Performance metrics under different scenarios
- Recommendations for fleet dimensioning
- Academic publication-ready results

## Timeline (2-4 weeks)

- Week 1: Environment setup, nominal flow modeling
- Week 2: Exceptional flows, resource models, basic simulation
- Week 3: Dispatching policies, experiments
- Week 4: Analysis, optimization, documentation

## Contact

For questions or improvements, refer to the project proposal document.
