# Prism

Modular CLI-first AI chat engine with streaming, persona switching, sliding-window memory, chat history, provider swapping, and per-session cost tracking. Built in versioned iterations toward a full web app.

---

## Features

- **Streaming responses** — output prints in real time as the model generates
- **Personas** — switch between `default`, `coder`, and `writer` mid-session
- **Sliding window memory** — retains the last 10 turns of context automatically
- **Cost tracking** — tracks input/output tokens and shows cost in USD and INR
- **Retry logic** — handles rate limits, timeouts, and connection errors gracefully

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/varsan-segar/prism.git
cd prism
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
.venv\Scripts\activate          # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
cp .env.example .env
```
Then open `.env` and fill in your API keys.

---

## Usage

```bash
python main.py
```

| Command | Description |
|---|---|
| `<message>` | Chat with the current persona |
| `/persona <name>` | Switch persona (`default`, `coder`, `writer`) |
| `/clear` | Reset conversation history |
| `/cost` | Show token usage and cost for the session |
| `/quit` | Exit |

---

## Project Structure

```
prism/
├── core/
│   ├── chat.py        # ChatEngine — orchestrates API, memory, and cost
│   ├── cost.py        # CostTracker — token usage and USD/INR cost calculation
│   └── memory.py      # SlidingWindowMemory — rolling conversation history
├── personas/
│   ├── default.json
│   ├── coder.json
│   └── writer.json
├── config.py          # Provider and model configuration
├── main.py            # Entry point and CLI loop
├── .env.example       # Environment variable template
└── requirements.txt
```

---

## Adding a Persona

Create a new JSON file in `personas/`:

```json
{
    "name": "your-persona",
    "system_prompt": "You are ..."
}
```

Then switch to it at runtime with `/persona your-persona`.

---

## Roadmap

- [ ] Groq provider support
- [ ] `/model` command to switch models mid-session
- [ ] Conversation export