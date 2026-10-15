


from traffic_input import get_vehicle_counts
from traffic_analyzer import analyze_traffic
from simulation import run_simulation
from performance_analyzer import generate_performance_report


def main():
    vehicle_counts = None
    signal_timings = None

    while True:
        print("\n===================================")
        print(" ADAPTIVE TRAFFIC SIGNAL SYSTEM")
        print("===================================")
        print("1. Enter Vehicle Counts")
        print("2. Analyze Traffic")
        print("3. Run Signal Simulation")
        print("4. View Performance Report")
        print("5. Exit")
        print("===================================")

        choice = input("Enter your choice (1-5): ").strip()
        if choice == "":
           print("Please enter a menu choice.")
           continue
        if choice == "1":
            vehicle_counts = get_vehicle_counts()

            # New counts require a new simulation.
            signal_timings = None

        elif choice == "2":
            if vehicle_counts is None:
                print("Please select option 1 and enter vehicle counts.")
            else:
                analyze_traffic(vehicle_counts)

        elif choice == "3":
            if vehicle_counts is None:
                print("Please select option 1 and enter vehicle counts.")
            else:
                # Clear any old timings before starting.
                signal_timings = None

                new_timings = run_simulation(vehicle_counts)

                if new_timings is not None:
                    signal_timings = new_timings
                    print("\nSimulation timings captured successfully.")
                else:
                    print(
                        "\nSimulation did not return valid timings. "
                        "The performance report cannot use this run."
                    )

        elif choice == "4":
            if vehicle_counts is None:
                print("Please enter vehicle counts first.")

            elif signal_timings is None:
                print(
                    "Please run option 3 and complete the simulation "
                    "before viewing the performance report."
                )

            else:
                generate_performance_report(
                    vehicle_counts,
                    signal_timings
                )

        elif choice == "5":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
