"""
INTRALOGISTICS SIMULATOR - RESULTS ANALYSIS
Readable analysis of the latest simulation run.
"""

import sys
from pathlib import Path

import pandas as pd
from tabulate import tabulate

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def pct(numerator, denominator):
    return (numerator / denominator * 100) if denominator else 0.0


def print_section(title):
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)


def main():
    print_section("INTRALOGISTICS SIMULATOR - RESULTS ANALYSIS")

    results_dir = Path("results")
    task_files = sorted(results_dir.glob("tasks_*.csv"))

    if not task_files:
        print("\nNo results found. Run this first:")
        print("   python main.py test")
        return 1

    latest_task_file = task_files[-1]
    tasks = pd.read_csv(latest_task_file)

    print(f"\nLoaded {len(tasks)} tasks from latest run")
    print(f"File: {latest_task_file.name}")

    on_time_count = int(tasks["on_time"].sum())
    total_count = len(tasks)
    service_level = pct(on_time_count, total_count)
    avg_lateness = tasks["lateness"].mean()
    max_lateness = tasks["lateness"].max()

    print_section("OVERALL PERFORMANCE")
    print(f"On-time delivery:  {on_time_count}/{total_count} tasks ({service_level:.1f}%)")
    print(f"Late deliveries:   {total_count - on_time_count} tasks ({100 - service_level:.1f}%)")
    print(f"Average lateness:  {avg_lateness:.2f} minutes")
    print(f"Maximum lateness:  {max_lateness:.2f} minutes")

    if service_level >= 95:
        print("Assessment: EXCELLENT - target service level achieved")
    elif service_level >= 85:
        print("Assessment: GOOD - acceptable performance")
    else:
        print("Assessment: NEEDS IMPROVEMENT - below target")

    print_section("NOMINAL VS EXCEPTIONAL FLOWS")
    flow_rows = []
    for flow_type in ["nominal", "exceptional"]:
        flow_tasks = tasks[tasks["flow_type"] == flow_type]
        flow_total = len(flow_tasks)
        if flow_total:
            flow_on_time = int(flow_tasks["on_time"].sum())
            flow_rows.append({
                "Flow Type": flow_type.upper(),
                "Total Tasks": flow_total,
                "On-Time": f"{flow_on_time}/{flow_total}",
                "On-Time %": f"{pct(flow_on_time, flow_total):.1f}%",
                "Avg Lateness": f"{flow_tasks['lateness'].mean():.2f} min",
            })

    print(tabulate(flow_rows, headers="keys", tablefmt="grid"))

    nominal_tasks = tasks[tasks["flow_type"] == "nominal"]
    exceptional_tasks = tasks[tasks["flow_type"] == "exceptional"]
    if len(nominal_tasks) and len(exceptional_tasks):
        impact = exceptional_tasks["lateness"].mean() - nominal_tasks["lateness"].mean()
        print(f"\nExceptional flow impact: {impact:+.2f} minutes additional lateness")

    print_section("TASK TYPE BREAKDOWN")
    task_rows = []
    for task_type in sorted(tasks["task_type"].unique()):
        subset = tasks[tasks["task_type"] == task_type]
        total = len(subset)
        on_time = int(subset["on_time"].sum())
        task_rows.append({
            "Task Type": task_type.upper(),
            "Count": total,
            "On-Time": f"{on_time}/{total}",
            "Success Rate": f"{pct(on_time, total):.1f}%",
            "Avg Delay": f"{subset['lateness'].mean():.2f} min",
        })
    print(tabulate(task_rows, headers="keys", tablefmt="grid"))

    print_section("RESOURCE ALLOCATION")
    resource_rows = []
    for resource in sorted(tasks["assigned_resource"].dropna().unique()):
        subset = tasks[tasks["assigned_resource"] == resource]
        total = len(subset)
        on_time = int(subset["on_time"].sum())
        resource_rows.append({
            "Resource": resource,
            "Tasks": total,
            "On-Time": on_time,
            "Success Rate": f"{pct(on_time, total):.1f}%",
            "Avg Lateness": f"{subset['lateness'].mean():.2f} min",
        })
    print(tabulate(resource_rows, headers="keys", tablefmt="grid"))

    print_section("LATENESS DISTRIBUTION")
    categories = {
        "On-time (0 min)": len(tasks[tasks["lateness"] == 0]),
        "Slightly late (1-5 min)": len(tasks[(tasks["lateness"] > 0) & (tasks["lateness"] <= 5)]),
        "Moderate late (6-15 min)": len(tasks[(tasks["lateness"] > 5) & (tasks["lateness"] <= 15)]),
        "Very late (16-30 min)": len(tasks[(tasks["lateness"] > 15) & (tasks["lateness"] <= 30)]),
        "Critical (>30 min)": len(tasks[tasks["lateness"] > 30]),
    }
    dist_rows = [
        {"Category": name, "Count": count, "Percentage": f"{pct(count, total_count):.1f}%"}
        for name, count in categories.items()
    ]
    print(tabulate(dist_rows, headers="keys", tablefmt="grid"))

    print_section("KEY RECOMMENDATIONS")
    if service_level >= 95:
        print("1. Service level is excellent for this run.")
    elif service_level >= 85:
        print("1. Service level is acceptable, but extra capacity or smarter dispatching may help.")
    else:
        print("1. Service level is below target; increase capacity or tune dispatching policy.")

    if len(exceptional_tasks):
        exceptional_success = pct(int(exceptional_tasks["on_time"].sum()), len(exceptional_tasks))
        print(f"2. Exceptional flow success: {exceptional_success:.1f}%.")

    critical_count = categories["Critical (>30 min)"]
    print(f"3. Critical late tasks (>30 min): {critical_count}.")

    print("\nRun full comparison any time with:")
    print("   python main.py comparison")
    print("\nAnalysis complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
