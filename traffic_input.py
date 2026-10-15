
def get_vehicle_counts():
    roads = ["North", "South", "East", "West"]
    vehicle_counts = {}

    print("\n===== ENTER VEHICLE COUNTS =====")

    for road in roads:
        while True:
            try:
                count = int(input(f"Enter vehicles on {road} road: "))

                if count < 0:
                    print("Vehicle count cannot be negative.")
                else:
                    vehicle_counts[road] = count
                    break

            except ValueError:
                print("Invalid input! Please enter a whole number.")

    print("\nVehicle counts saved successfully!")
    return vehicle_counts
