import json
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel

from .chat_config import MAX_TOKENS, MODEL, TEMPERATURE, build_system_prompt

load_dotenv()

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
jinja_env = Environment(
    loader=FileSystemLoader(str(BASE_DIR / "templates")),
    autoescape=select_autoescape(["html"]),
)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

ai_client = anthropic.Anthropic()

SITE = {
    "linkedin": "https://www.linkedin.com/in/tom-m-62489317b/",
    "email": "tom@flintagentic.co.uk",
    "whatsapp": "https://wa.me/447587759704",
}

ABOUT_ME = (
    "After 18 years in the Royal Marines — including operational logistics and specialist "
    "vehicle operations — I've swapped ranks for repositories. I'm now building Flint "
    "Agentic, designing practical AI agents that handle the repetitive work so businesses "
    "can focus on what actually needs a human touch. The same things that mattered on "
    "operations still matter here: discipline, clear communication, and getting the job "
    "done properly rather than just quickly.\n\n"
    "Outside of work, you'll find me out running, sketching, or watching Bolton Wanderers "
    "do their best to keep me on my toes. It's the same mindset in a different kit — "
    "showing up consistently, paying attention to detail, and enjoying the process as much "
    "as the result."
)


def load_json(filename: str):
    with open(BASE_DIR / "data" / filename, encoding="utf-8") as f:
        return json.load(f)


def load_text(filename: str) -> str:
    return (BASE_DIR / "data" / filename).read_text(encoding="utf-8")


@app.get("/", response_class=HTMLResponse)
def index():
    news = sorted(load_json("news.json"), key=lambda item: item["date"], reverse=True)
    template = jinja_env.get_template("index.html")
    return template.render(
        site=SITE,
        about_me=ABOUT_ME,
        agents=load_json("agents.json"),
        news=news,
    )


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []


@app.post("/api/chat")
def chat(payload: ChatRequest):
    messages = [{"role": m.role, "content": m.content} for m in payload.history]
    messages.append({"role": "user", "content": payload.message})

    response = ai_client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        system=build_system_prompt(load_text("knowledge.md")),
        messages=messages,
    )
    return {"reply": response.content[0].text}
