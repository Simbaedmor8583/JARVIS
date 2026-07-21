# JARVIS — Local Desktop AI Assistant

JARVIS is a Windows desktop voice assistant that combines local speech and routing models with an optional OpenRouter-powered cloud model. It can launch and control applications, automate browser and Office tasks, manage email and WhatsApp workflows, play media, research topics, and respond through speech.

The project is under active development. Treat automation that sends messages, moves files, or controls the operating system with appropriate care.

## What the project does

- Listens for the “Hey Jarvis” wake phrase and accepts spoken commands.
- Uses a fast rule-based lane and a local Qwen router to select actions.
- Supports speech-to-text, text-to-speech, and interruption while speaking.
- Controls Windows applications, volume, media, windows, and common system actions.
- Automates browser, Gmail, WhatsApp, Word, Excel, and PowerPoint workflows.
- Provides research, news, memory, file search, and desktop organization skills.
- Uses OpenRouter for optional cloud conversation, drafting, research, and summaries.

## Requirements

- Windows 11
- 64-bit Python 3.11 or 3.12
- A microphone and speakers or headphones
- Approximately 4 GB of free disk space for downloaded models and Chromium
- An OpenRouter API key if you want cloud-backed features

## How to install it

Open Command Prompt or PowerShell in the project directory:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install torch==2.4.1 --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
python -m playwright install chromium
```

Create a local `.env` file in the project root and add only the settings you need:

```dotenv
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=deepseek/deepseek-v4-flash
```

For SMTP/IMAP fallback, you may also configure `EMAIL_ADDRESS` and `EMAIL_APP_PASSWORD`. Never commit `.env`, API keys, app passwords, browser profiles, or other credentials. They are intentionally excluded by `.gitignore`.

The first run may download the wake-word model, Whisper model, local router model, and browser components.

## How to run it

Start the full voice assistant:

```powershell
python main.py
```

Run without wake-word or text-to-speech support:

```powershell
python main.py --text-only
```

Useful diagnostic options include `--debug` for full tracebacks and `--skip-model-preload` for a faster startup check.

To run the automated tests:

```powershell
python -m pytest
```

To build the Windows executable:

```powershell
.\build_exe.bat
```

Generated executables and build output are not stored in the repository.

## Current problems

- Wake-word and “stop” detection can pick up speaker echo; headphones work best.
- Gmail and WhatsApp automation can break when their user interfaces change.
- WhatsApp workflows require the desktop application to be installed and linked.
- The small local routing model can misclassify unusual phrasing.
- First-run setup is large and slow because several models and browser components are downloaded.
- Hardware, microphone, Windows permissions, and third-party service differences need broader testing.

## Features we need help with

- More reliable Gmail, WhatsApp, and browser selectors and recovery paths.
- Better routing accuracy, intent coverage, and multilingual commands.
- Improved wake-word, barge-in, and noisy-room behavior.
- Automated setup, dependency checks, and clearer first-run diagnostics.
- More unit and integration tests, especially for failure and safety paths.
- Accessibility improvements and testing across different Windows configurations.
- Documentation for adding new skills and supported automation targets.

## Contributing

Issues, fixes, and feature proposals are welcome.

1. Open an issue for significant changes so the approach can be discussed first.
2. Fork the repository and create a focused branch from `main`.
3. Make a small, well-scoped change and add or update tests.
4. Run `python -m pytest` and document any tests that cannot run locally.
5. Confirm your commit contains no secrets, `.env` files, credentials, personal data, logs, databases, browser profiles, generated builds, or downloaded models.
6. Submit a pull request describing the problem, the solution, testing performed, and any user-visible behavior changes.

Do not include real API keys, OpenRouter credentials, email app passwords, private keys, or private documents in issues, commits, test fixtures, screenshots, or pull requests.

## Safety notes

JARVIS can interact with applications and operating-system functions. Review configuration carefully and keep confirmation prompts enabled for sensitive actions such as sending messages or shutting down the computer. Test automation with non-sensitive accounts and files whenever possible.
