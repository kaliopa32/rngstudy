import csv
import os
from datetime import datetime

LOG_FILE = "log.txt"
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

def new_run_id() -> str:
   # time used for roll uid
    return datetime.now().strftime("%Y%m%d-%H%M%S")


