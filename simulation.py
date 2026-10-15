

from signal_controller import calculate_signal_timings

ROADS = ["North", "South", "East", "West"]
YELLOW_SECONDS = 3


def get_seconds(value):
    """Convert a timing value into an integer number of seconds."""
    if isinstance(value, (int, float)):
        return int(value)

    if isinstance(value, str):
        import re
        match = re.search(r"\d+", value)
        if match:
            return int(match.group())

    return None


def run_simulation(vehicle_counts):
    """Run the signal simulation and return its actual timings."""

    print("\n===== STARTING TRAFFIC SIMULATION =====")

    # Calculate timings using the existing signal controller.
    raw_timings = calculate_signal_timings(vehicle_counts)

    if not isinstance(raw_timings, dict):
        print("Error: Signal controller did not return timing data.")
        return None

    # Standardise road names and timing values.
    signal_timings = {}

    for road in ROADS:
        for key, value in raw_timings.items():
            key_name = (
                str(key).lower().replace(" ", "").replace("_", "")
            )

            if key_name in (road.lower(), road.lower() + "road"):
                seconds = get_seconds(value)

                if seconds is not None and seconds > 0:
                    signal_timings[road] = seconds
                break

    if len(signal_timings) != 4:
        print("Error: Could not obtain timings for all four roads.")
        return None

    print("\n===== ADAPTIVE SIGNAL TIMINGS =====")

    for road in ROADS:
        print(
            f"{road} Road: GREEN for "
            f"{signal_timings[road]} seconds"
        )

    # Display each road's signal sequence.
    for active_road in ROADS:
        print(f"\n{active_road} Road Signal Sequence:")
        print("\n===== TRAFFIC SIGNAL STATUS =====")

        for road in ROADS:
            status = "GREEN" if road == active_road else "RED"
            print(f"{road} Road: {status}")

        print(
            f"Green signal duration: "
            f"{signal_timings[active_road]} seconds"
        )

        print(f"{active_road} Road: YELLOW")
        print(f"Yellow signal duration: {YELLOW_SECONDS} seconds")

        print(f"{active_road} Road: RED")
        print("Signal phase completed.")

    print("\n===== SIMULATION COMPLETED =====")

    # IMPORTANT: Return the same timings for the performance report.
    return signal_timings
