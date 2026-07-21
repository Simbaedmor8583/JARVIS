# JARVIS â€” Local Desktop AI Assistant (Windows 11)

A complete, locally-running JARVIS-style voice assistant. Two brains (a local
Qwen router + OpenRouter cloud brain), a fast rule lane for instant commands,
full voice pipeline (offline wake word, faster-whisper STT, edge-tts voice),
and 14 pluggable skills covering apps, browser, email, news, music, WhatsApp,
Office documents, desktop organization, app building and deep research.

Say **"Hey Jarvis"** â€” it answers, listens, acts, and reports back.

---

## 1. Requirements

- Windows 11, Python **3.11 or 3.12** (64-bit)
- A microphone + speakers (headphones recommended â€” see "Barge-in" below)
- The default cloud model is `deepseek/deepseek-v4-flash` through OpenRouter (set `OPENROUTER_MODEL` to change).

An **OpenRouter API key** (https://openrouter.ai) for the cloud brain
- ~4 GB free disk for models on first run (Whisper + Qwen + Chromium)

## 2. Setup (development mode)

```bat
cd JARVIS
python -m venv .venv
.venv\Scripts\activate

REM smaller/faster CPU-only torch first (recommended):
pip install torch==2.4.1 --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

REM Playwright browser:
python -m playwright install chromium

REM secrets:
copy .env.example .env
notepad .env        REM put your OPENROUTER_API_KEY in

python main.py
```

First run downloads: the `hey_jarvis` wake-word model (auto), the Whisper
`base` model (~150 MB), and Qwen2.5-0.5B-Instruct (~1 GB) from Hugging Face.
After that everything is cached.

## 3. Building the .exe

```bat
build_exe.bat
```

Output: `dist\JARVIS.exe` â€” single file, console window shows heard text,
intent, action and result. The exe runs from anywhere and still treats your
Desktop as home base. Notes:

- Secrets are never embedded. Place `.env` next to `JARVIS.exe`; it is loaded
  at startup and can be changed without rebuilding.
- Playwright's Chromium is **not** embedded (keeps the exe lean); on first
  browser use JARVIS auto-downloads it (`playwright install chromium`).
- The wake-word model and Python packages are bundled via `--collect-all`.

## 4. Gmail setup

**Browser mode (default, recommended):** the first time you say "check my
email", a Chromium window opens Gmail. Log in once within 60 seconds â€” the
profile persists forever after (it lives in `data/browser_profile`).

**SMTP/IMAP fallback:** only needed if the Gmail UI ever fails.
1. Google Account â†’ Security â†’ enable 2-Step Verification.
2. Search "App passwords" â†’ create one named JARVIS â†’ copy the 16-char code.
3. Put `EMAIL_ADDRESS` and `EMAIL_APP_PASSWORD` in `.env`.

## 5. Talking to JARVIS

Wake phrase: **"Hey Jarvis"** â†’ it replies "Yes, sir?" â†’ speak your command.
Barge-in: say **"Jarvis stop"** (or just "stop") while it's talking.

| You say | What happens |
|---|---|
| open notepad / open youtube / open my resume | universal opener (app â†’ file â†’ folder â†’ site) |
| close it / close YouTube / close everything you opened | Session Registry teardown |
| volume up / mute / screenshot / lock the pc / status report | system control |
| shut down / restart / sleep the computer | voice-confirmed power control |
| play music | asks what you're in the mood for, then plays it on YouTube |
| play lana del rey | straight to playback |
| pause / resume / next video / stop the music | music controls |
| check my email / read the email from Sara | Gmail in the browser |
| write an email to Ahmed about the meeting | drafts â†’ reads it aloud â†’ confirms â†’ sends |
| what's the latest news / tech news / UAE news | spoken briefing from RSS feeds |
| tell me more about the third one | fetches + summarizes that article |
| save the news | .docx briefing on your Desktop |
| let's do research on X | deep-research mode: discuss â†’ outline â†’ sources â†’ draft â†’ Word doc |
| open whatsapp / read messages from Mom / reply to all unread | WhatsApp Desktop automation |
| write an essay about X in Word | .docx on Desktop, opens visibly in Word |
| create a spreadsheet of monthly expenses | .xlsx with headers + formulas, opens in Excel |
| create a presentation about X with 10 slides | .pptx, opens in PowerPoint |
| organize my desktop / undo organize | sorts files into category folders, fully reversible |
| open codex and create an app that does X | Codex CLI in a new terminal (or generates the code itself) |
| search for X | Google results tab |
| remember that I take tea at 4 | persistent memory (data/memory.json) |
| anything else | conversation with memory, JARVIS personality |

## 6. Safety

Voice confirmation is required before: sending emails, sending WhatsApp
messages, deleting anything, shutdown. Everything else executes immediately.

- `CONFIRM_SENDS=false` in `.env` disables all confirmations.
- `AUTO_SEND=true` auto-sends WhatsApp replies (use carefully).
- The Desktop Organizer **never deletes** â€” moves only, all logged, undoable.

## 7. Architecture

```
main.py                wake loop + orchestration + console log
config.py              .env loading, paths, flags
brain/router.py        rule-based fast lane + local Qwen2.5-0.5B classifier
brain/llm.py           OpenRouter client (OpenAI-compatible, streaming)
brain/prompts.py       router / personality / research / drafting prompts
voice/wakeword.py      openwakeword "hey_jarvis" (offline)
voice/listener.py      faster-whisper + webrtcvad silence detection
voice/speaker.py       edge-tts + pygame, threaded, barge-in stop
voice/pipeline.py      reusable complete voice-pipeline facade
core/registry.py       Session Registry â€” everything JARVIS opened
skills/*.py            14 pluggable skill modules
data/                  registry, memory, logs, research session, browser profile
```

Command pipeline: **pending state â†’ fast lane (regex, 0 ms) â†’ Qwen router
(local, <1 s) â†’ skill dispatch**. The cloud brain is only used for
conversation, drafting, research and summaries â€” never for routing.

## 8. Notes & limitations

- **Barge-in accuracy:** the "stop" monitor listens through your mic while
  JARVIS speaks. Speakers can echo into the mic â€” headphones make it crisp.
- **WhatsApp/Gmail UI automation** is best-effort by nature (their UIs change);
  every step has fallbacks and speaks clearly if something fails.
- **WhatsApp Desktop** must be installed and logged in (phone linked).
- `python main.py --text-only` runs without wake-word or TTS. Add `--debug`
  when you want full exception tracebacks during development.
- `python main.py --skip-model-preload` skips background Whisper/router
  preload for faster startup checks; models still load when first used.
- Edge TTS is preferred, with automatic offline Piper fallback on HTTP 403
  and all other network or synthesis errors.
- Router model is small on purpose (fast). If it mis-routes an odd phrasing,
  rephrase slightly â€” or say the fast-lane phrasing from the table above.
