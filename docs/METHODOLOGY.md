# METHODOLOGY: Intralogistics Simulation Framework

## 1. SIMULATION MODELING APPROACH

### 1.1 Discrete-Event Simulation (DES)

The simulator uses **SimPy**, a Python discrete-event simulation library, to model:
- **Entities**: Tasks (jobs), Resources (equipment/operators)
- **Events**: Task arrivals, task processing, resource state changes
- **State**: Queue lengths, resource utilization, task status

### 1.2 Simulation Clock

- Time unit: **1 minute**
- Default duration: **480 minutes** (8-hour production shift)
- Continuous time axis (events trigger at precise times)

---

## 2. SYSTEM MODEL

### 2.1 Scope Definition

**Intralogistics Perimeter:**
```
Warehouse → Supermarket → Line-side Feeding → Production Line → Returns
```

**Key Locations:**
- Warehouse: Central inventory
- Supermarket: Decoupled point-of-use storage
- Line: Production assembly point
- Quality/Rework: Exception handling area

### 2.2 Flows

#### Nominal Flows
- **Characteristics**: Planned, scheduled, predictable
- **Volume**: 85-100% of workload (configurable)
- **Variability**: Low (known assembly schedules)
- **Urgency**: Standard (30-120 min due time)
- **Example tasks**: Standard kit picks, regular deliveries

#### Exceptional Flows
- **Characteristics**: Unplanned, reactive, urgent
- **Volume**: 0-30% of workload (configurable)
- **Variability**: High (quality failures, late changes, shortages)
- **Urgency**: High (5-30 min due time)
- **Example tasks**: Rush picks, rework, quality returns, missing items

---

## 3. HETEROGENEOUS RESOURCES

### 3.1 Resource Types

#### Automated Resources (AGV - Autonomous Guided Vehicle)
```python
Properties:
  - Speed: 20 tasks/hour
  - Reliability: 95% uptime
  - Flexibility: Low (fixed routes)
  - Capacity: 10 tasks in queue
  - Cost: €50/hour
  - Processing time: 50% faster than manual
  - Variability: Low (deterministic)
```

#### Semi-Automated Resources (Conveyor/Robotic System)
```python
Properties:
  - Speed: 15 tasks/hour
  - Reliability: 92% uptime
  - Flexibility: Medium
  - Capacity: 20 tasks in queue
  - Cost: €30/hour
  - Processing time: 20% faster than manual
  - Variability: Medium (some variation)
```

#### Manual Resources (Human Operators)
```python
Properties:
  - Speed: 10 tasks/hour
  - Reliability: 85% uptime (breaks, fatigue)
  - Flexibility: High (any task)
  - Capacity: 5 tasks in queue
  - Cost: €20-25/hour
  - Processing time: Baseline
  - Variability: High (human variability ±20%)
```

### 3.2 Resource Characteristics

| Feature | Automated | Semi-Auto | Manual |
|---------|-----------|-----------|--------|
| **Speed** | High | Medium | Low |
| **Reliability** | High | Medium | Low |
| **Flexibility** | Low | Medium | High |
| **Variability** | Low | Medium | High |
| **Cost** | High CAPEX | Medium | Low CAPEX |

---

## 4. DISPATCHING POLICIES

### 4.1 Policy Descriptions

#### 1. FIFO (First-In-First-Out) - Baseline
```
Logic:
  - All tasks served in arrival order
  - No prioritization
  - Assign to least busy resource
  
Behavior:
  - Stable, predictable
  - Fair but not optimized
  - Exceptional tasks wait behind nominal tasks
  
Use Case:
  - Baseline for comparison
  - Simple implementation
```

#### 2. Priority-Based
```
Logic:
  - Exceptional tasks get priority over nominal
  - Within flow type: urgent > high > normal > low
  - Assign to fastest available resource for urgent tasks
  
Behavior:
  - Exceptional tasks processed faster
  - Nominal tasks may wait longer
  - Better exceptional flow performance
  
Use Case:
  - Mixed nominal + exceptional workload
  - When exceptions are business-critical
```

#### 3. Load-Balancing
```
Logic:
  - Always assign to least-busy resource
  - Minimize maximum queue length
  - Distribute evenly across fleet
  
Behavior:
  - Smooth resource utilization
  - Reduced peak queues
  - Better average lateness
  
Use Case:
  - Homogeneous resources
  - Smoothing demand spikes
```

#### 4. Preemptive
```
Logic:
  - URGENT tasks can preempt normal tasks
  - High priority gets fastest resource
  - Mid-priority uses secondary resources
  
Behavior:
  - Minimal exceptional task lateness
  - Risk of starvation for low-priority
  - Highest recovery capability
  
Use Case:
  - High cost of service failures
  - Quality/safety critical exceptions
```

#### 5. Adaptive (Advanced)
```
Logic:
  - Switch strategy based on system state:
    * High queue → Load balance
    * Many urgent tasks → Priority-based
    * Normal → Standard balance
  
Behavior:
  - Responsive to changing conditions
  - Self-regulating
  - Best for variable conditions
  
Use Case:
  - Highly variable workload
  - Long simulation horizons
```

---

## 5. SIMULATION SCENARIOS

### 5.1 Scenario Definitions

#### Scenario 1: Baseline (Nominal Only)
```
Purpose: Establish performance ceiling
Configuration:
  - Nominal tasks only (100% of workload)
  - No resource unavailability
  - Standard demand rate (10 tasks/hour)
  
Metrics Used:
  - Service level (should be ~100%)
  - Baseline lateness
```

#### Scenario 2: Mixed Flows - 15% Exceptional
```
Purpose: Typical operations
Configuration:
  - 85% nominal + 15% exceptional
  - Normal resource availability
  - Standard demand
  
Metrics Used:
  - Service level comparison
  - Nominal vs exceptional performance
  - Policy effectiveness
```

#### Scenario 3: Mixed Flows - 30% Exceptional
```
Purpose: High-exception environment
Configuration:
  - 70% nominal + 30% exceptional
  - Normal resource availability
  
Metrics Used:
  - Policy resilience
  - Saturation effects
  - Exceptional flow dominance
```

#### Scenario 4: Resource Unavailability (10% Down)
```
Purpose: Robustness test
Configuration:
  - 15% exceptional flows
  - One resource unavailable (90% of fleet)
  
Metrics Used:
  - Recovery capability
  - Queue buildup
  - Lateness impact
```

#### Scenario 5: Demand Spike (1.5x Normal)
```
Purpose: Peak demand handling
Configuration:
  - 1.5x normal task arrival rate
  - 15% exceptional flows
  - All resources available
  
Metrics Used:
  - Saturation point
  - Queue behavior
  - Capacity adequacy
```

---

## 6. PERFORMANCE METRICS

### 6.1 Service Level Metrics

**On-Time Delivery Rate (Service Level)**
$$SL = \frac{\text{Tasks completed by due time}}{\text{Total tasks completed}} \times 100\%$$
- Target: ≥ 95%
- Indicates customer satisfaction

**Average Lateness**
$$AL = \frac{\sum \max(0, C_i - D_i)}{n}$$
- Where: $C_i$ = completion time, $D_i$ = due time
- Lower is better (measured in minutes)

**Maximum Lateness**
$$ML = \max(C_i - D_i)$$
- Indicates worst-case performance
- Critical for meeting critical deadlines

### 6.2 Resource Utilization Metrics

**Resource Utilization**
$$U = \frac{\text{Time busy}}{\text{Total time}} \times 100\%$$
- Typical target: 75-85%
- Too low: Overcapacity | Too high: Congestion

**Average Queue Length**
$$AQL = \frac{\sum Q_i}{n}$$
- $Q_i$ = queue length at time i
- Indicates congestion level

**Maximum Queue Length**
$$MQL = \max(Q_i)$$
- Worst-case congestion
- Affects storage space needs

### 6.3 Resilience Metrics

**Robustness Index**
$$R = \frac{SL/100 + (1 - \frac{\sigma}{100})}{2}$$
- Combined service level + variance measure
- Range: 0-1, higher is better
- Measures consistent performance

**Exceptional Flow Impact**
$$EI = AL_{exceptional} - AL_{nominal}$$
- Additional lateness caused by exceptions
- Positive = exceptions cause delays
- Negative = exceptions accelerated by resource focus

**Recovery Capability**
$$RC = \frac{\text{Lateness reduced after spike}}{\text{Peak lateness during spike}}$$
- Measures system's ability to absorb and recover
- Higher = better resilience

---

## 7. EXPERIMENTAL DESIGN

### 7.1 Comparison Matrix

```
┌──────────────────────────────────────┬─────────┬──────────┬───────────────┐
│ Scenario                             │ FIFO    │ Priority │ Preemptive    │
├──────────────────────────────────────┼─────────┼──────────┼───────────────┤
│ Baseline (Nominal)                   │    A    │    A     │      A        │
│ Mixed 15% Exceptional                │    B    │    B+    │      B++      │
│ Mixed 30% Exceptional                │    C    │    C+    │      C++      │
│ Resource Unavailable (10%)           │    D-   │    D     │      D+       │
│ Demand Spike (1.5x)                  │    E-   │    E     │      E+       │
└──────────────────────────────────────┴─────────┴──────────┴───────────────┘
Legend: A/B/C/D/E = Performance level (A = best)
        +/- = Relative improvement
```

### 7.2 Simulation Runs

- **Runs per scenario**: 3-5 replications (for confidence intervals)
- **Random seed**: Different for each replication
- **Duration**: 480 minutes per run
- **Warmup**: First 60 minutes (transient behavior)

### 7.3 Analysis Methods

1. **Descriptive Statistics**: Mean, std dev, min, max
2. **Comparative Analysis**: Policy vs policy (t-tests)
3. **Sensitivity Analysis**: Vary exceptional ratio, speed, availability
4. **Time-Series Analysis**: Queue length, utilization over time
5. **Visualization**: Line plots, heatmaps, box plots

---

## 8. VALIDATION & VERIFICATION

### 8.1 Verification Checklist

- [ ] Tasks complete with realistic processing times
- [ ] Queue lengths decrease when resources are idle
- [ ] Lateness never negative (can't complete before due time)
- [ ] Resource utilization correlates with queue length
- [ ] Exceptional tasks have shorter due times
- [ ] Service level ≈ 100% for nominal-only scenario

### 8.2 Sensitivity Analysis

Test impact of varying:
- Exceptional ratio (0%, 15%, 30%, 50%)
- Resource speed variability (±5%, ±20%)
- Number of resources (2, 3, 4, 5)
- Demand rate (8, 10, 12, 15 tasks/hour)

---

## 9. OUTPUT & REPORTING

### 9.1 Outputs Generated

```
results/
├── tasks_*.csv                    # Detailed task data
├── results_*.csv                  # Metrics summary
├── comparison_summary_*.json      # Cross-scenario comparison
├── plots/
│   ├── service_level_comparison.png
│   ├── queue_length_timeline.png
│   └── utilization_heatmap.png
└── report_*.txt                   # Executive summary
```

### 9.2 Key Findings to Extract

1. **Best policy** for each scenario
2. **Exceptional flow impact** quantification
3. **Capacity recommendations** (optimal fleet size)
4. **Trade-offs** (cost vs service level)
5. **Robustness gaps** (where resilience is weak)

---

## 10. EXTENSIONS & FUTURE WORK

### 10.1 Advanced Features

- Multi-period scheduling (shift changes, breaks)
- Machine learning for dynamic policy selection
- Optimization via genetic algorithms
- Real-time interactive dashboard
- What-if scenario analysis

### 10.2 Model Enhancements

- Spatial routing (actual distances)
- Resource-specific capabilities (can only handle certain tasks)
- Batch processing (group multiple tasks)
- Learning/adaptation (resources improving over time)
- Stochastic resource failures

---

**Document Version**: 1.0  
**Last Updated**: 2026-06-04  
**Framework**: SimPy (Python)
