from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
NOTES_DIR = BASE_DIR / "notes"


def list_notes():
    # Ensure the notes directory exists so commands behave predictably
    try:
        NOTES_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        # If creation fails, fall back to reporting no notes
        return []

    return sorted([path.name for path in NOTES_DIR.iterdir() if path.is_file()])


def read_note(filename):
    path = NOTES_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Note '{filename}' was not found in {NOTES_DIR}.")

    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        raise IOError(f"Unable to read note '{filename}': {exc}") from exc
