
from datetime import datetime
import rng
import logger

def read_roll_count() -> int:
    while True:
        s = input("How many rolls? (positive integer): ").strip()
        try:
            n = int(s)
            if n <= 0:
                print("Enter a number > 0.")
                continue
            return n
        except ValueError:
            print("Enter a valid integer.")

def main() -> None:
    count = read_roll_count()
    run_id = logger.new_run_id()

    for i in range(1, count + 1):
        r = rng.roll()

        logger.log({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "run_id": run_id,
            "roll_index": i,
            "final": r["final"],
            "base": r["base"],
            "roll": r["roll"],
            "modifier": r["modifier"],
        })

    logger.print_latest_rolls(count)

if __name__ == "__main__":
    main()





















































