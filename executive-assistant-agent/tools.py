from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
NOTES_DIR = BASE_DIR / "notes"


def list_notes():
    if not NOTES_DIR.exists():
        return []
    return sorted([path.name for path in NOTES_DIR.iterdir() if path.is_file()])


def read_note(filename):
    path = NOTES_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Note '{filename}' was not found.")
    return path.read_text(encoding="utf-8")
