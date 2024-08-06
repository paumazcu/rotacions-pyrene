import tools
import time


def run():
    success = False
    attempts = 0
    max_attempts = 500

    while not success and attempts < max_attempts:
        attempts += 1
        try:
            prova, nits_counts, meals_counts, tl_counts, total_counts = tools.assign_names_to_tasks()
            success = True
            for d in prova.items():
                print(d)

            print("\n NITS\n", nits_counts)
            print("\n MEALS\n", meals_counts)
            print("\n TL\n", tl_counts)
            print("\n TOTALS\n", total_counts)

        except Exception as e:
            print(f"Attempt {attempts} failed: {e}. Trying again...")

    if not success:
        print("Failed to complete the algorithm after maximum attempts.")

if __name__ == "__main__":
    run()