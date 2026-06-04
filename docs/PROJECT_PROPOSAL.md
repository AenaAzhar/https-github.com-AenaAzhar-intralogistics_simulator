# PROJECT PROPOSAL
# Mini Intralogistics Simulator: Heterogeneous Fleet Management for Resilient Intralogistics

## 1. EXECUTIVE SUMMARY

This project develops a discrete-event simulation (DES) framework to model and compare heterogeneous intralogistics systems under nominal production flows combined with exceptional flows (late replanning, quality events, rework). The focus is on aerospace line-side logistics, including warehouse-to-line picking, kitting, supermarkets, line feeding, and returns management.

**Key Objective**: Evaluate how dispatching policies, resource allocation, and capacity configuration affect robustness and resilience when facing both predictable and unpredictable demand.

## 2. SCIENTIFIC CONTEXT

### 2.1 Problem Statement

In aerospace manufacturing (and similar industries):
- **Nominal flows** follow planned production schedules and are relatively predictable
- **Exceptional flows** (quality returns, late replanning, missing items) are unpredictable but critical
- **Current practice**: Intralogistics dimensioned for nominal flows only → frequent shortages, micro-stops, poor service
- **Challenge**: How to design and control systems that maintain performance under both nominal and exceptional conditions?

### 2.2 Research Gap

Limited research on:
- Quantifying the impact of exceptional flows on intralogistics performance
- Comparing dispatching strategies for mixed nominal + exceptional workloads
- Dimensioning heterogeneous resources (automated, semi-automated, manual) under uncertainty

## 3. RESEARCH OBJECTIVES

1. **Model heterogeneous intralogistics** coupling nominal flows, exceptional flows, diverse resources
2. **Compare dispatching policies** (FIFO, priority-based, preemptive, pooling strategies)
3. **Assess resilience** under uncertainty, resource unavailability, demand volatility
4. **Identify levers** for improving robustness without excessive cost overhead

## 4. METHODOLOGY

### 4.1 Simulation Approach

**Discrete-Event Simulation (DES)** using Python/SimPy:
- Entities: Tasks (nominal & exceptional), Resources (AGV, conveyor, operator), Locations (warehouse, supermarket, line)
- Events: Task arrival, task pickup, task delivery, resource availability change
- State variables: Queue lengths, resource utilization, service level, task delays

### 4.2 System Model

**Scope**: Warehouse → Supermarket → Line-side feeding → Returns

**Resources (Heterogeneous Fleet)**:
- Automated (AGV): Fast, reliable, limited capacity, high CAPEX
- Semi-automated (Conveyor): Medium speed, good throughput, inflexible
- Manual (Operator): Flexible, variable speed, labor cost

**Flow Types**:
- **Nominal**: Scheduled kits, predictable volumes, standard routing
- **Exceptional**: Urgent picks, rework, quality returns, high priority

**Performance Indicators**:
- Service level (% of on-time deliveries)
- Delivery lateness (avg, max)
- Resource utilization
- Queue lengths
- Capacity slack needed for robustness

### 4.3 Experiments

**Scenario 1**: Baseline - nominal flows only
**Scenario 2**: Mixed nominal + exceptional (10%, 20%, 30% of workload)
**Scenario 3**: Resource unavailability (1 resource down 5%, 10%)
**Scenario 4**: Demand spike (150%, 200% of normal)

**Dispatching Policies**:
1. FIFO: First-in-first-out (baseline)
2. Priority-based: Nominal < Exceptional
3. Load-balancing: Minimize queue lengths
4. Preemptive: Pause non-critical tasks for urgent ones

### 4.4 Outputs

- Comparative tables: Policy performance across scenarios
- Time-series graphs: Queue lengths, utilization, lateness over time
- Heatmaps: Sensitivity analysis (workload % vs service level)
- Recommendations: Policy selection, capacity guidelines

## 5. EXPECTED DELIVERABLES

### 5.1 Code & Models
- ✓ Modular DES framework (environment, resources, flows, dispatcher, metrics)
- ✓ 4 dispatching policy implementations
- ✓ Configurable scenarios and parameters

### 5.2 Data
- ✓ Synthetic dataset: 1,000+ nominal & exceptional tasks
- ✓ Resource specifications (speed, capacity, cost, reliability)
- ✓ Configuration file for easy scenario setup

### 5.3 Documentation
- ✓ README with quick start guide
- ✓ Methodology document (this file)
- ✓ Code comments and docstrings
- ✓ Results template for reporting findings

### 5.4 Results
- ✓ Simulation output data (CSV)
- ✓ Performance comparison tables
- ✓ Graphs and visualization
- ✓ Summary report with insights

## 6. RELEVANCE TO PhD POSITION

This project demonstrates:
- ✓ Understanding of intralogistics complexity (nominal + exceptional flows)
- ✓ Competence with discrete-event simulation
- ✓ Ability to model heterogeneous resources
- ✓ Skills in dispatching and resource allocation problems
- ✓ Capacity for applied research on industrial systems
- ✓ Clear problem structuring and experimental design

## 7. TIMELINE (2-4 Weeks)

| Week | Milestones |
|------|-----------|
| **Week 1** | Environment setup; Nominal flow model; Basic task generation |
| **Week 2** | Exceptional flow model; Heterogeneous resource models; Base simulator |
| **Week 3** | Dispatching policies; Scenario experiments; Preliminary results |
| **Week 4** | Analysis; Visualization; Documentation; Final report |

## 8. SUCCESS CRITERIA

- ✓ Simulator runs without errors for 100+ tasks across multiple policies
- ✓ Results show clear differences between policies (not all identical)
- ✓ At least 1 exceptional flow scenario tested
- ✓ At least 3 performance metrics tracked
- ✓ Code is modular, documented, and reproducible
- ✓ Results are saved and visualized
- ✓ Report identifies at least 3 actionable insights

## 9. ADVANCED EXTENSIONS (Optional)

If time permits:
- Machine learning for adaptive dispatch
- Optimization via genetic algorithms
- Agent-based modeling (comparison with DES)
- Real-time dashboard (Dash, Streamlit)
- Sensitivity analysis on key parameters

---

**Project Owner**: PhD Candidate in Heterogeneous Fleet Management for Intralogistics

**Date Created**: 2026-06-04
