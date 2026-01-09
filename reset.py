import os

LOG_FILE = "log.txt"
RUN_ID_FILE = "run_id.txt"


def _prompt_yes_no(prompt: str) -> bool:
    answer = input(prompt).strip().lower()
    if answer in {"y", "yes"}:
        return True
    if answer in {"n", "no", ""}:
        return False
    print("Please enter 'yes' or 'no'.")
    return _prompt_yes_no(prompt)


def _remove_if_exists(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)
        print(f"Removed {path}.")
    else:
        print(f"{path} not found.")


def main() -> None:
    if _prompt_yes_no("Reset logs (default: no)? [y/N]: "):
        _remove_if_exists(LOG_FILE)
        _remove_if_exists(RUN_ID_FILE)
        print("Reset complete.")
    else:
        print("No changes made.")


if __name__ == "__main__":
    main()
