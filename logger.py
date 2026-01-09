import csv
import os
from datetime import datetime

LOG_FILE = "log.txt"
RUN_ID_FILE = "run_id.txt"
FIELDS = ["timestamp", "run_id", "roll_index", "final", "base", "roll", "modifier"]
COLUMN_WIDTHS = {
    "timestamp": 19,
    "run_id": 6,
    "roll_index": 10,
    "final": 8,
    "base": 6,
    "roll": 8,
    "modifier": 9,
}
RIGHT_ALIGN_FIELDS = {"run_id", "roll_index", "final", "base", "roll", "modifier"}
SEPARATOR = "  "

def _format_row(row: dict) -> str:
    parts = []
    for field in FIELDS:
        width = COLUMN_WIDTHS[field]
        value = str(row.get(field, ""))
        value = value[:width]
        if field in RIGHT_ALIGN_FIELDS:
            parts.append(value.rjust(width))
        else:
            parts.append(value.ljust(width))
    return SEPARATOR.join(parts)

def _parse_fixed_width_line(line: str) -> dict:
    row = {}
    idx = 0
    for field in FIELDS:
        width = COLUMN_WIDTHS[field]
        row[field] = line[idx:idx + width].strip()
        idx += width + len(SEPARATOR)
    return row

def _read_rows(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, "r", newline="", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    if not lines:
        return []
    header = lines[0]
    if "," in header:
        with open(path, "r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    return [_parse_fixed_width_line(line) for line in lines[1:] if line.strip()]

def _rewrite_csv_to_fixed_width(path: str) -> None:
    rows = _read_rows(path)
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(_format_row({field: field for field in FIELDS}) + "\n")
        for row in rows:
            f.write(_format_row(row) + "\n")

def log(row: dict, path: str = LOG_FILE) -> None:
    """
    Appends one fixed-width line per call.
    Creates the file (and writes a header) if it doesn't exist yet.
    """
    file_exists = os.path.exists(path)

    # Ensure all fields exist (missing -> "")
    out = {k: row.get(k, "") for k in FIELDS}

    if file_exists:
        with open(path, "r", newline="", encoding="utf-8") as f:
            first_line = f.readline().strip()
        if first_line and "," in first_line:
            _rewrite_csv_to_fixed_width(path)
    else:
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write(_format_row({field: field for field in FIELDS}) + "\n")

    with open(path, "a", newline="", encoding="utf-8") as f:
        f.write(_format_row(out) + "\n")

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

    rows = _read_rows(path)

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


