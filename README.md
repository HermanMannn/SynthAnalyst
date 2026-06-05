# SynthAnalyst Intelligence Engine 🧠

An AI-powered competitive intelligence agent that analyzes competitor websites and generates personalized cold outreach emails — triggered directly from Slack.

## What It Does

Send `/analyze https://competitor.com` in Slack and the agent will:

1. **Scrape** the competitor's website
2. **Analyze** their value proposition and identify product weaknesses (via CrewAI + Gemini)
3. **Draft** a targeted cold outreach email exploiting those weaknesses
4. **Post the results** back to your Slack channel automatically

No need to open a terminal or browser — just send the command and wait for the response.

---

## Architecture

```
Slack /analyze command
        ↓
    ngrok tunnel
        ↓
    n8n Webhook
        ↓
FastAPI /api/analyze
        ↓
  CrewAI Agents (Gemini 2.5 Flash)
  ├── Agent 1: Competitive Intelligence Analyst
  └── Agent 2: Enterprise Sales Copywriter
        ↓
  Posts result to Slack channel
```

---

## Stack

| Layer | Tech |
|---|---|
| AI Agents | [CrewAI](https://crewai.com) |
| LLM | Google Gemini 2.5 Flash |
| Web Scraping | LangChain `WebBaseLoader` |
| API Server | FastAPI + Uvicorn |
| Workflow Automation | [n8n](https://n8n.io) |
| Slack Integration | Slack Slash Commands + Bot API |
| Tunnel (dev) | ngrok |

---

## Prerequisites

- Python 3.10+
- n8n running locally on port 5678
- ngrok installed
- A Slack app with a slash command and `chat:write` scope
- Google Gemini API key
- Slack Bot Token (`xoxb-...`)

---

## Setup

### 1. Clone & install dependencies

```bash
git clone https://github.com/yourusername/synthanalyst.git
cd synthanalyst
pip install fastapi uvicorn python-dotenv crewai langchain-community httpx
```

### 2. Create your `.env` file

```env
GEMINI_API_KEY=your-gemini-api-key
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
```

### 3. Configure your Slack app

1. Go to [api.slack.com/apps](https://api.slack.com/apps) and create a new app
2. Under **OAuth & Permissions**, add the `chat:write` scope
3. Under **Slash Commands**, create a new command:
   - Command: `/analyze`
   - Request URL: `https://your-ngrok-url/webhook/your-webhook-id`
4. Install the app to your workspace and copy the **Bot User OAuth Token**

### 4. Configure n8n

Import the workflow and make sure:
- The **Webhook** node is set to respond **Immediately**
- The **HTTP Request** node points to `http://127.0.0.1:8000/api/analyze`
- The body sends `competitor_url` mapped to `{{ $json.text }}`
- The workflow is set to **Active**

---

## Running

Double-click `start.bat` or run manually:

```bash
# Terminal 1 — FastAPI
python main.py

# Terminal 2 — ngrok (tunnel to n8n)
ngrok http 5678
```

### Persistent URL (recommended)

Get a free static ngrok domain at [dashboard.ngrok.com/domains](https://dashboard.ngrok.com/domains) so your Slack slash command URL never changes:

```bash
ngrok http --domain=your-static-domain.ngrok-free.app 5678
```

---

## Usage

In any Slack channel the bot is added to:

```
/analyze https://competitor.com
```

Optionally specify a target role:

```
/analyze https://competitor.com Head of Engineering
```

Results will be posted to the channel within 1–2 minutes.

---

## Project Structure

```
synthanalyst/
├── app.py          # FastAPI server + CrewAI agent logic
├── start.bat        # One-click startup script
├── .env             # API keys (never commit this)
├── .env.example     # Template for .env
└── README.md
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key from [aistudio.google.com](https://aistudio.google.com) |
| `SLACK_BOT_TOKEN` | Slack bot token starting with `xoxb-` |

---

## How the Agent Works

Two CrewAI agents run sequentially:

**Agent 1 — Competitive Intelligence Analyst**
Reads the scraped website content and extracts the competitor's core value proposition plus three likely product weaknesses or customer pain points.

**Agent 2 — Enterprise Sales Copywriter**
Takes the analyst's report and drafts a cold outreach email targeting a specified role, positioning your solutions against the competitor's weaknesses without being aggressive.

---

## Limitations

- Free ngrok restarts generate a new URL — update your Slack slash command URL or use a static domain
- Website scraping is limited to the first 2000 characters of the homepage
- Slack messages are capped at 2900 characters; longer reports are truncated

---
