

def calculate_signal_timings(vehicle_counts):
    min_green_time = 10
    max_green_time = 60
    total_vehicles = sum(vehicle_counts.values())
    signal_timings = {}

    for road, count in vehicle_counts.items():
        if total_vehicles == 0:
            green_time = min_green_time
        else:
            green_time = int(
                (count / total_vehicles) * max_green_time
            )
            green_time = max(min_green_time, green_time)
            green_time = min(max_green_time, green_time)

        signal_timings[road] = green_time

    return signal_timings


def display_signal_timings(signal_timings):
    print("\n===== ADAPTIVE SIGNAL TIMINGS =====")

    for road, green_time in signal_timings.items():
        print(f"{road} Road: GREEN for {green_time} seconds")


def display_signal_status(active_road):
    roads = ["North", "South", "East", "West"]

    print("\n===== TRAFFIC SIGNAL STATUS =====")

    for road in roads:
        if road == active_road:
            print(f"{road} Road: GREEN")
        else:
            print(f"{road} Road: RED")
