# Flint Agentic — flintagentic.com

The personal site for Flint Agentic: hero, About Me, an "Agents Built So Far" gallery,
an "Ask Flint" chat assistant, and a News/Updates feed. Built with FastAPI + Jinja2,
deployed to Render — same pattern as [lead-agent](https://github.com/TomFlintAgentic/lead-agent).

## Project structure

```
flintagentic-com/
├── app/
│   ├── main.py            # FastAPI app — routes, page rendering, /api/chat
│   ├── chat_config.py      # Ask Flint system prompt template + tunables (model, tone, length)
│   ├── data/
│   │   ├── agents.json     # "Agents Built So Far" cards
│   │   ├── news.json       # News/Updates entries
│   │   └── knowledge.md    # Ask Flint's only source of truth about Tom/services
│   ├── templates/
│   │   └── index.html      # The single-page site
│   └── static/
│       ├── css/style.css
│       └── js/main.js       # Ask Flint chat widget logic
├── requirements.txt
├── Procfile                # Render start command
└── .env.example
```

## Adding a new agent card

Open [app/data/agents.json](app/data/agents.json) and append an object:

```json
{
  "name": "New Agent Name",
  "repo_url": "https://github.com/TomFlintAgentic/new-agent-repo",
  "description": "One or two sentences on what it does."
}
```

No HTML or CSS changes needed — the card grid renders automatically.

## Adding a news update

Open [app/data/news.json](app/data/news.json) and append an object:

```json
{
  "title": "Short headline",
  "date": "2026-07-13",
  "summary": "2-3 sentence summary, e.g. scaled down from the weekly Agent Recon report."
}
```

Entries are shown newest-first automatically (sorted by `date`).

## Editing what Ask Flint knows

Ask Flint only answers from [app/data/knowledge.md](app/data/knowledge.md) — it will
not use the model's general knowledge about Tom or Flint Agentic. To teach it
something new (career details, a new FAQ, a service update), just edit that file
and push; no code changes needed.

If a visitor asks something outside the knowledge base, Ask Flint politely says so
and asks for their name and email instead of guessing — it never invents an answer.

## Adjusting the Ask Flint chat widget's tone or behaviour

Everything else about the chatbot — its tone, model, and contact-capture phrasing —
lives in [app/chat_config.py](app/chat_config.py). Edit `SYSTEM_PROMPT_TEMPLATE`,
`MODEL`, `MAX_TOKENS`, or `TEMPERATURE` there — no other code needs to change.

## Local development

```bash
python -m venv venv
venv/Scripts/activate      # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your-anthropic-api-key
```

Run it:

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000`.

## Deployment (Render)

1. Push this repo to GitHub.
2. In Render, create a new **Web Service** from the GitHub repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT` (already in the Procfile, Render should detect it automatically).
5. Instance type: **Free**.
6. Add environment variable: `ANTHROPIC_API_KEY`.
7. Once deployed, go to the service's **Settings → Custom Domains** and add `flintagentic.com` (and `www.flintagentic.com` if wanted). Render will give you a DNS record (CNAME/ALIAS) to add at your domain registrar (123-reg).
8. Wait for DNS to propagate and Render to issue the free TLS certificate.

## Author

Built by Tom Flint — Flint Agentic.
