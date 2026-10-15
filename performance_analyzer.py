

import os
import re
from datetime import datetime

ROADS = ["North", "South", "East", "West"]

YELLOW_SECONDS = 3
FIXED_GREEN_SECONDS = 30

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


def normalize_road_name(name):
    """Convert names like 'North Road' or 'North' to 'North'."""
    name = re.sub(r"[^a-z]", "", str(name).lower())

    if name.endswith("road"):
        name = name[:-4]

    return name.title()


def convert_to_seconds(value):
    """Convert an integer or text such as '10 seconds' into seconds."""
    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        seconds = int(value)
    else:
        match = re.search(r"\d+", str(value))

        if not match:
            return None

        seconds = int(match.group())

    if seconds <= 0:
        return None

    return seconds


def normalize_vehicle_counts(vehicle_counts):
    """Validate vehicle counts for all four roads."""
    if not isinstance(vehicle_counts, dict):
        return None

    counts = {}

    for name, value in vehicle_counts.items():
        road = normalize_road_name(name)

        if road not in ROADS:
            continue

        if isinstance(value, bool):
            return None

        try:
            count = int(value)
        except (TypeError, ValueError):
            return None

        if count < 0:
            return None

        counts[road] = count

    if any(road not in counts for road in ROADS):
        return None

    return counts


def normalize_signal_timings(signal_timings):
    """
    Use the actual timings returned by simulation.py.
    Do not calculate replacement timings here.
    """
    if not isinstance(signal_timings, dict):
        return None

    timings = {}

    for name, value in signal_timings.items():
        road = normalize_road_name(name)

        if road not in ROADS:
            continue

        seconds = convert_to_seconds(value)

        if seconds is not None:
            timings[road] = seconds

    if any(road not in timings for road in ROADS):
        return None

    return timings


def calculate_waiting_times(green_timings):
    """
    Estimate average waiting time using this project's simplified model.

    Cycle length = total green time + all yellow phases.
    Estimated wait = (cycle length - road green time - yellow time) / 2.
    """
    cycle_length = (
        sum(green_timings.values())
        + len(ROADS) * YELLOW_SECONDS
    )

    waiting_times = {}

    for road in ROADS:
        non_green_time = (
            cycle_length
            - green_timings[road]
            - YELLOW_SECONDS
        )

        waiting_times[road] = max(0, non_green_time / 2)

    return waiting_times, cycle_length


def calculate_weighted_average(waiting_times, vehicle_counts):
    """Calculate average waiting time weighted by vehicle count."""
    total_vehicles = sum(vehicle_counts.values())

    if total_vehicles == 0:
        return None

    total_waiting_time = sum(
        vehicle_counts[road] * waiting_times[road]
        for road in ROADS
    )

    return total_waiting_time / total_vehicles


def generate_performance_report(vehicle_counts, signal_timings=None):
    counts = normalize_vehicle_counts(vehicle_counts)

    if counts is None:
        print("ERROR: Valid vehicle counts for all four roads are required.")
        return None

    # Important: use only the timings returned by the simulation.
    adaptive_green = normalize_signal_timings(signal_timings)

    if adaptive_green is None:
        print("\nERROR: Actual signal timings are not available.")
        print("Please select option 3 and complete the simulation first.")
        print("The report has not been generated.")
        return None

    # Calculate adaptive waiting times from the actual simulation timings.
    adaptive_waits, adaptive_cycle = calculate_waiting_times(
        adaptive_green
    )

    # Fixed-time strategy: every road receives 30 seconds of green.
    fixed_green = {
        road: FIXED_GREEN_SECONDS for road in ROADS
    }

    fixed_waits, fixed_cycle = calculate_waiting_times(fixed_green)

    adaptive_average = calculate_weighted_average(
        adaptive_waits, counts
    )

    fixed_average = calculate_weighted_average(
        fixed_waits, counts
    )

    # Build the report.
    lines = [
        "==========================================",
        "       TRAFFIC PERFORMANCE REPORT",
        "==========================================",
        "",
        "NOTE: Waiting times are estimates from a simplified model,",
        "not measurements of real-world traffic.",
        "",
        f"Total vehicles: {sum(counts.values())}",
        "",
        "VEHICLE COUNTS:",
    ]

    for road in ROADS:
        lines.append(f"{road} Road: {counts[road]} vehicles")

    lines.extend([
        "",
        "==========================================",
        "ADAPTIVE STRATEGY",
        "==========================================",
        "Green timings used from the actual simulation:",
    ])

    for road in ROADS:
        lines.append(
            f"{road} Road: Green for {adaptive_green[road]} seconds"
        )

    lines.extend([
        f"Adaptive cycle length: {adaptive_cycle} seconds",
        "",
        "Estimated waiting times:",
    ])

    for road in ROADS:
        lines.append(
            f"{road} Road: {adaptive_waits[road]:.1f} seconds"
        )

    lines.extend([
        "",
        "==========================================",
        "FIXED-TIME STRATEGY",
        "==========================================",
        f"Green time per road: {FIXED_GREEN_SECONDS} seconds",
        f"Fixed cycle length: {fixed_cycle} seconds",
        "",
        "Estimated waiting times:",
    ])

    for road in ROADS:
        lines.append(
            f"{road} Road: {fixed_waits[road]:.1f} seconds"
        )

    lines.extend([
        "",
        "==========================================",
        "PERFORMANCE COMPARISON",
        "==========================================",
    ])

    if fixed_average is None or adaptive_average is None:
        lines.append(
            "Weighted average cannot be calculated because "
            "there are no vehicles."
        )
    else:
        lines.append(
            f"Fixed-time weighted average wait: "
            f"{fixed_average:.2f} seconds per vehicle"
        )

        lines.append(
            f"Adaptive weighted average wait: "
            f"{adaptive_average:.2f} seconds per vehicle"
        )

        if fixed_average > 0:
            change_percent = (
                (fixed_average - adaptive_average)
                / fixed_average
            ) * 100

            if change_percent >= 0:
                lines.append(
                    f"Estimated waiting-time reduction: "
                    f"{change_percent:.1f}%"
                )
            else:
                lines.append(
                    f"Estimated waiting-time increase: "
                    f"{abs(change_percent):.1f}%"
                )

    lines.append("")
    lines.append("==========================================")

    report = "\n".join(lines)

    # Display the report.
    print("\n" + report)

    
    # Append every report to ONE file.
    try:
        os.makedirs(REPORTS_DIR, exist_ok=True)

        report_path = os.path.join(
            REPORTS_DIR,
            "performance_report.txt"
        )

        timestamp = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        file_is_not_empty = (
            os.path.exists(report_path)
            and os.path.getsize(report_path) > 0
        )

        with open(report_path, "a", encoding="utf-8") as file:
            if file_is_not_empty:
                file.write("\n\n" + "=" * 60 + "\n\n")

            file.write(f"REPORT GENERATED: {timestamp}\n\n")
            file.write(report)
            file.write("\n")

        print("\nReport appended successfully.")
        print(f"All reports are stored in: {report_path}")

    except OSError as error:
        print(f"\nERROR: Could not save the report: {error}")

    return report
