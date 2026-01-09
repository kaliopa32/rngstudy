import csv
import os
from datetime import datetime

LOG_FILE = "log.txt"
RUN_ID_FILE = "run_id.txt"
FIELDS = ["timestamp", "run_id", "roll_index", "final", "base", "roll", "modifier"]

def log(row: dict, path: str = LOG_FILE) -> None:
    """
    Appends one CSV-formatted line per call.
    Creates the file (and writes a header) if it doesn't exist yet.
    """
    file_exists = os.path.exists(path)

    # Ensure all fields exist (missing -> "")
    out = {k: row.get(k, "") for k in FIELDS}

    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if not file_exists:
            w.writeheader()
        w.writerow(out)

def new_run_id(path: str = RUN_ID_FILE) -> int:
    """
    Returns the next run id, persisted in a counter file.
    """
    last_id = 0
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                last_id = int(f.read().strip() or "0")
        except (OSError, ValueError):
            last_id = 0

    next_id = last_id + 1
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(next_id))
    return next_id

def print_latest_rolls(count: int, path: str = LOG_FILE) -> None:
    """
    Prints the latest N rolls from the log file.
    """
    if count <= 0:
        print("No rolls to display.")
        return
    if not os.path.exists(path):
        print("No log file found.")
        return

    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("No rolls logged yet.")
        return

    for row in rows[-count:]:
        print(
            f"run {row.get('run_id', '')} roll {row.get('roll_index', '')}: "
            f"final={row.get('final', '')}, "
            f"base={row.get('base', '')}, "
            f"roll={row.get('roll', '')}, "
            f"modifier={row.get('modifier', '')}"
        )


