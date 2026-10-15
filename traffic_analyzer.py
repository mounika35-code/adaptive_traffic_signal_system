

"""Traffic analysis for the Adaptive Traffic Signal System."""

ROADS = ["North", "South", "East", "West"]


def get_traffic_level(vehicle_count):
    """Classify traffic based on vehicle count."""
    if vehicle_count <= 20:
        return "LOW"
    elif vehicle_count <= 40:
        return "MEDIUM"
    else:
        return "HIGH"


def analyze_traffic(vehicle_counts):
    """Display traffic levels and identify all busiest roads."""

    # Accept both short names and names containing 'Road'.
    counts = {}

    for road in ROADS:
        count = 0

        for key, value in vehicle_counts.items():
            normalised_key = (
                str(key).lower().replace(" ", "").replace("_", "")
            )

            if normalised_key in (road.lower(), road.lower() + "road"):
                try:
                    count = max(0, int(value))
                except (ValueError, TypeError):
                    count = 0
                break

        counts[road] = count

    print("\n===== TRAFFIC ANALYSIS =====")

    for road in ROADS:
        count = counts[road]
        level = get_traffic_level(count)

        print(f"{road} Road: {count} vehicles - {level} traffic")

    highest_count = max(counts.values())

    if highest_count == 0:
        print("\nNo vehicles have been recorded.")
        busiest_roads = []
    else:
        busiest_roads = [
            road for road in ROADS
            if counts[road] == highest_count
        ]

        if len(busiest_roads) == 1:
            print(f"\nBusiest Road: {busiest_roads[0]}")
            print(f"Vehicle Count: {highest_count} vehicles")
        else:
            print("\nBusiest Roads (tie): " + ", ".join(busiest_roads))
            print(f"Vehicle Count: {highest_count} vehicles each")

    return {
        "vehicle_counts": counts,
        "traffic_levels": {
            road: get_traffic_level(counts[road])
            for road in ROADS
        },
        "busiest_roads": busiest_roads,
        "highest_count": highest_count,
    }
