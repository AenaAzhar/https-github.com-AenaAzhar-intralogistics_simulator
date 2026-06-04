# RESULTS REPORTING TEMPLATE
# Use this template to document findings from simulation runs

## Run Information

| Parameter | Value |
|-----------|-------|
| **Date** | YYYY-MM-DD HH:MM:SS |
| **Scenario** | [e.g., Mixed Flows 15% Exceptional] |
| **Policy Tested** | [e.g., Priority-Based] |
| **Duration** | 480 minutes |
| **Replication** | Run X of Y |

---

## Key Performance Indicators

### Service Level

| Metric | Baseline | Tested Policy | Difference |
|--------|----------|---------------|-----------|
| **Overall On-Time %** | XX.X% | XX.X% | +/- X.X% |
| **Nominal On-Time %** | XX.X% | XX.X% | +/- X.X% |
| **Exceptional On-Time %** | XX.X% | XX.X% | +/- X.X% |
| **Avg Lateness (min)** | XX.XX | XX.XX | +/- XX.XX |
| **Max Lateness (min)** | XXX | XXX | +/- XXX |

### Resource Utilization

| Resource | FIFO | Priority | Load Bal | Preemptive |
|----------|------|----------|----------|------------|
| **AGV_1** | XX% | XX% | XX% | XX% |
| **CONV_1** | XX% | XX% | XX% | XX% |
| **OP_1** | XX% | XX% | XX% | XX% |
| **OP_2** | XX% | XX% | XX% | XX% |
| **Average** | XX% | XX% | XX% | XX% |

### Queue Management

| Metric | Value |
|--------|-------|
| **Avg Queue Length** | X.XX tasks |
| **Max Queue Length** | XX tasks |
| **% Time Queue > 5** | XX% |
| **% Time Queue > 10** | XX% |

### Exceptional Flow Impact

| Metric | Value |
|--------|-------|
| **Nominal Avg Lateness** | XX.XX min |
| **Exceptional Avg Lateness** | XX.XX min |
| **Impact** | +XX.XX min |
| **Impact %** | +XX% |

### Resilience

| Metric | Value |
|--------|-------|
| **Robustness Index** | X.XX / 1.00 |
| **Performance Variance** | XX.XX |
| **Recovery Time (after spike)** | XX minutes |

---

## Analysis & Observations

### What Worked Well
- Observation 1: ...
- Observation 2: ...
- Observation 3: ...

### Challenges Encountered
- Challenge 1: ...
- Challenge 2: ...
- Challenge 3: ...

### Policy Effectiveness

**vs FIFO Baseline:**
- ✓ Better: [metrics that improved]
- ✗ Worse: [metrics that degraded]
- ≈ Same: [metrics that stayed similar]

**Specific Advantages:**
1. ...
2. ...

**Specific Disadvantages:**
1. ...
2. ...

---

## Scenario-Specific Findings

### Exceptional Flow Handling
- How well does policy handle 15% / 30% exceptional workload?
- Does service differentiation work as intended?
- Trade-offs between nominal and exceptional performance?

### Resource Efficiency
- Are resources balanced across fleet?
- Any bottleneck resources?
- Utilization appropriate (75-85% range)?

### Peak Demand Handling
- Queue behavior during demand spike?
- Recovery time after spike?
- Did any resources saturate?

---

## Quantitative Comparison

```
Service Level Comparison (Scenario: Mixed 15% Exceptional)

FIFO:        ████████░░  84.5%
Priority:    ██████████  95.2%  (+10.7%)
LoadBal:     █████████░  92.1%  (+7.6%)
Preemptive:  ██████████  96.8%  (+12.3%)

Average Lateness (minutes)

FIFO:        ████████░░  12.3 min
Priority:    ████░░░░░░   5.8 min  (-52.8%)
LoadBal:     ██████░░░░   7.2 min  (-41.5%)
Preemptive:  ███░░░░░░░   4.1 min  (-66.7%)
```

---

## Recommendations

### For This Scenario:
1. **Recommended Policy**: [FIFO / Priority / LoadBal / Preemptive / Adaptive]
   - **Justification**: ...
   - **Expected Performance**: ...

2. **Fleet Configuration**:
   - Number of each resource type: ...
   - Suggested capabilities: ...
   - Estimated cost/benefit: ...

3. **Operational Guidelines**:
   - When to use this policy: ...
   - When to switch policies: ...
   - Key parameters to monitor: ...

### For Future Work:
1. Test with [different scenario]
2. Explore [alternative approach]
3. Validate assumptions on [parameter]

---

## Statistical Summary

### Sample Size & Confidence
- Replication runs: [X]
- Mean values: [computed from X runs]
- 95% Confidence Interval: [lower, upper]
- Coefficient of Variation: XX%

### Statistical Tests
- ANOVA F-statistic: F = X.XX, p = 0.0XX
- Conclusion: [Policies are / are not significantly different]

---

## Appendix A: Detailed Metrics Table

| Task ID | Flow Type | Arrival | Due | Completion | Lateness | On-Time | Resource |
|---------|-----------|---------|-----|------------|----------|---------|----------|
| 1 | Nominal | 0 | 45 | 38 | 0 | ✓ | AGV_1 |
| 2 | Nominal | 5 | 50 | 52 | 2 | ✗ | CONV_1 |
| 3 | Exceptional | 8 | 25 | 23 | 0 | ✓ | AGV_1 |
| ... | ... | ... | ... | ... | ... | ... | ... |

---

## Appendix B: Time-Series Data

[Include plots/data if available:]
- Queue length over time graph
- Resource utilization timeline
- Task lateness distribution
- Performance trends

---

**Report Prepared By**: [Name/Role]  
**Date Prepared**: YYYY-MM-DD  
**Data Files**: [List CSV exports]  
**Code Version**: 0.1.0
