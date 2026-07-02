# Executive Assistant Agent

This project is a simple CLI-based executive assistant that uses a local Ollama model to help with meeting preparation, notes, and follow-up drafting.

## What this project does

The agent can:

- list notes stored in the notes folder
- read a specific note
- send general prompts to a local LLM
- help prepare for meetings from your notes
- draft follow-up emails

## Install Ollama

Install Ollama from the official site:
https://ollama.com/

After installation, start the service:

```bash
ollama serve
```

## Pull the model

Pull the required model:

```bash
ollama pull llama3
```

## Install Python dependencies

```bash
pip install -r requirements.txt
```

## Run the agent

```bash
python agent.py
```

## Example commands

```text
list notes
read note meeting1.txt
prepare meeting
write follow up email
```
