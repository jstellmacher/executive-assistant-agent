import requests
from pathlib import Path

from tools import list_notes, read_note

SYSTEM_PROMPT = "You are an executive assistant that helps with meetings, prep, notes, and follow-up."
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3"
BASE_DIR = Path(__file__).resolve().parent
NOTES_DIR = BASE_DIR / "notes"


def call_ollama(prompt):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError("Ollama is not running. Start it with 'ollama serve' and make sure the model is available.") from exc
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Unable to reach Ollama: {exc}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(f"Invalid JSON response from Ollama: {exc}") from exc

    # Ollama's response payload may vary; defensively extract content
    # Common structure: { "message": { "content": "..." } }
    message = data.get("message") if isinstance(data, dict) else None
    if isinstance(message, dict):
        return str(message.get("content", "")).strip()

    # Fallback: try to extract a top-level 'content' or return full body
    if isinstance(data, dict) and "content" in data:
        return str(data.get("content", "")).strip()

    return str(data).strip()


def prepare_meeting():
    notes = list_notes()
    if not notes:
        return "No notes were found in the notes folder, so there is nothing to summarize."

    collected = []
    skipped = []
    for name in notes:
        try:
            content = read_note(name)
            collected.append(f"Note: {name}\n{content}")
        except Exception:
            skipped.append(name)

    if not collected:
        return "Found notes, but none could be read. Check file permissions."

    note_text = "\n\n".join(collected)
    prompt = (
        "Based on the following meeting notes, generate:\n"
        "- a meeting summary\n"
        "- talking points\n"
        "- action items\n\n"
        f"{note_text}\n\n"
        + (f"(Skipped unreadable notes: {', '.join(skipped)})" if skipped else "")
    )

    try:
        return call_ollama(prompt)
    except RuntimeError:
        raise


def write_follow_up_email():
    notes = list_notes()
    if not notes:
        return "No notes found in the notes folder to generate a follow-up email."

    # Determine most recently modified note file
    note_paths = [NOTES_DIR / name for name in notes]
    try:
        latest = max(note_paths, key=lambda p: p.stat().st_mtime)
    except Exception:
        latest = note_paths[0]

    filename = latest.name
    try:
        note_content = read_note(filename)
    except Exception as exc:
        return f"Unable to read the latest note '{filename}': {exc}"

    prompt = (
        f"You are a professional assistant. Write a concise, professional follow-up email "
        f"based on the meeting note titled '{filename}'. Include a greeting, a brief summary, "
        "action items/next steps, and a polite closing. Keep it suitable for a business audience.\n\n"
        f"Meeting note:\n{note_content}\n\n"
    )

    try:
        return call_ollama(prompt)
    except RuntimeError:
        raise


def main():
    print("Executive Assistant Agent")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        command = user_input.lower()

        if command == "list notes":
            notes = list_notes()
            if not notes:
                print("No notes found in the notes folder.")
            else:
                print("Available notes:")
                for note in notes:
                    print(f"- {note}")
            continue

        if command.startswith("read note "):
            filename = user_input[len("read note "):].strip()
            try:
                content = read_note(filename)
            except FileNotFoundError as exc:
                print(f"Error: {exc}")
            else:
                print(content)
            continue

        if command == "prepare meeting":
            try:
                response = prepare_meeting()
            except RuntimeError as exc:
                print(f"Error: {exc}")
            else:
                print(f"Assistant: {response}")
            continue

        if command in {"write follow up email", "write follow-up email"}:
            try:
                response = write_follow_up_email()
            except RuntimeError as exc:
                print(f"Error: {exc}")
            else:
                print(f"Assistant: {response}")
            continue

        try:
            response = call_ollama(user_input)
        except RuntimeError as exc:
            print(f"Error: {exc}")
        else:
            print(f"Assistant: {response}")


if __name__ == "__main__":
    main()
