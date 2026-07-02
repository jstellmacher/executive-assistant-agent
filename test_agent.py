import agent
from tools import list_notes, read_note

# Mock the LLM call to avoid requiring Ollama for verification
agent.call_ollama = lambda prompt: "MOCK_RESPONSE:\n" + "(model received prompt)"

print("--- list_notes ---")
print(list_notes())

print("\n--- read_note meeting1.txt ---")
try:
    print(read_note('meeting1.txt'))
except Exception as e:
    print('Error reading note:', e)

print("\n--- prepare_meeting ---")
try:
    print(agent.prepare_meeting())
except Exception as e:
    print('prepare_meeting error:', e)

print("\n--- write_follow_up_email ---")
try:
    print(agent.write_follow_up_email())
except Exception as e:
    print('write_follow_up_email error:', e)
