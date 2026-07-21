"""
Conversation & Memory — free discussion with short-term context
(last ~20 exchanges) plus a persistent memory.json for facts about you
("remember that I prefer tea"). Smalltalk is instant and model-free.
"""
import json
import time
from collections import deque

from config import Config
from brain.prompts import JARVIS_SYSTEM_PROMPT

_history = deque(maxlen=Config.CHAT_HISTORY_TURNS * 2)


# ---------------------------------------------------------------------------
# Persistent memory
# ---------------------------------------------------------------------------
def _load_memory():
    try:
        if Config.MEMORY_FILE.exists():
            data = json.loads(Config.MEMORY_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("facts", [])
                return data
    except Exception:
        pass
    return {"facts": []}


def _save_memory(data):
    try:
        Config.MEMORY_FILE.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def remember(fact, ctx):
    fact = (fact or "").strip()
    if not fact:
        return "Remember what, sir?"
    data = _load_memory()
    if fact.lower() not in [f.lower() for f in data["facts"]]:
        data["facts"].append(fact)
        _save_memory(data)
    return f"Noted, sir. I'll remember that {fact}."


def _memory_block():
    facts = _load_memory().get("facts", [])
    if not facts:
        return "(none yet)"
    return "\n".join(f"- {f}" for f in facts[-30:])


# ---------------------------------------------------------------------------
# Conversation
# ---------------------------------------------------------------------------
def chat(message, remember_fact, ctx):
    if remember_fact:
        return remember(remember_fact, ctx)

    message = (message or "").strip()
    if not message:
        return "Yes, sir?"

    if not ctx.llm.available:
        return _offline_reply(message)

    system = JARVIS_SYSTEM_PROMPT.format(
        address=Config.OWNER_ADDRESS, memory=_memory_block())
    messages = [{"role": "system", "content": system}]
    messages.extend(list(_history))
    messages.append({"role": "user", "content": message})

    reply = ctx.llm.chat(messages, temperature=0.75, max_tokens=450)
    if not reply:
        return _offline_reply(message)

    _history.append({"role": "user", "content": message})
    _history.append({"role": "assistant", "content": reply})
    return reply


def _offline_reply(message):
    """Useful local response when OpenRouter is unavailable."""
    low = message.lower()
    if any(word in low for word in ("help", "what can you do", "capabilities")):
        return (
            "Cloud reasoning is offline, sir, but local controls remain available: "
            "apps, files, music, browser, volume, power, news feeds, and Office tasks."
        )
    if "who are you" in low:
        return "I'm JARVIS, your local Windows assistant, currently in offline mode, sir."
    return (
        "The cloud reasoning service is unavailable, sir. Local commands still work; "
        "conversation, drafting, and summarization will resume when the connection returns."
    )


# ---------------------------------------------------------------------------
# Smalltalk — instant, zero model calls
# ---------------------------------------------------------------------------
def smalltalk(kind, ctx):
    a = Config.OWNER_ADDRESS
    kind = (kind or "").lower()
    if kind == "greeting":
        hour = time.localtime().tm_hour
        daypart = ("morning" if hour < 12 else
                   "afternoon" if hour < 18 else "evening")
        return f"Good {daypart}, {a}. How may I assist?"
    if kind == "thanks":
        return f"You're welcome, {a}."
    if kind == "howareyou":
        return f"All systems running smoothly, {a} — thank you for asking. And you?"
    if kind == "goodbye":
        return f"Very good, {a}. I'll be here when you need me."
    if kind == "time":
        return f"It's {time.strftime('%H:%M')}, {a}."
    if kind == "date":
        return f"Today is {time.strftime('%A, %d %B %Y')}, {a}."
    return f"Yes, {a}?"


# ---------------------------------------------------------------------------
# Skill dispatch entry
# ---------------------------------------------------------------------------
def handle(intent, ctx):
    skill = intent.get("skill")
    params = intent.get("params", {}) or {}
    if skill == "chat":
        return chat(params.get("message", ""), params.get("remember", ""), ctx)
    if skill == "smalltalk":
        return smalltalk(params.get("kind", ""), ctx)
    return None
