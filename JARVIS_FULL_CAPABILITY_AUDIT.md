# JARVIS Full Capability Audit

## Generated: July 19, 2026
## Project: C:\Users\Burab\OneDrive\Desktop\JARVIS

---

## 1. PROJECT STRUCTURE

### Entry Points

| File | Purpose | Active In |
|------|---------|-----------|
| desktop_main.py | PySide6 GUI entry point. Launches PySide6 window, tray, controller, background model preload. | Final GUI build (JARVIS-GUI.spec) |
| main.py | Console/voice entry point. Wake-word loop, typed fallback, command orchestration. | Source mode only (JARVIS.spec) |
| config.py | Loads .env, defines all paths, secrets, constants. Central import for every module. | Both |
| JARVIS-GUI.spec | PyInstaller spec for windowed GUI build (console=False). | Build target |
| JARVIS.spec | PyInstaller spec for console build (console=True). | Build target |
| build_exe.bat | Batch build script. Pins torch CPU, downloads models, runs watchdog build. | Build |


### Core Packages

| File | Purpose | Main Classes/Functions | Active In |
|------|---------|----------------------|-----------|
| brain/llm.py | OpenRouter API client (OpenAI-compatible) | LLM class: chat(), stream(), quick(), quick_json(), test_connection() | Both |
| brain/router.py | Intent routing: fast-lane regex + local Qwen classifier | fast_lane(), Router.classify() | Both |
| brain/prompts.py | All prompt templates | ROUTER_SYSTEM_PROMPT, JARVIS_SYSTEM_PROMPT, research/news/email/office prompts | Both |
| core/registry.py | Session Registry - tracks all opened items | SessionRegistry class: register(), close_by_name(), close_all(), close_most_recent() | Both |
| core/planner.py | Deterministic multi-step plan builder | plan_command() handles compound commands | Both |
| core/assistant_controller.py | Backend controller bridging GUI and services | AssistantController: start_voice(), stop_voice(), handle_text(), shutdown() | Both |
| core/settings.py | GUI settings persistence to %%LOCALAPPDATA%%/JARVIS/config.json | SettingsStore class | Both |
| core/command_text.py | Voice command normalization | cleanup_command() | Both |
| core/desktop_agent.py | Unified desktop automation (mouse, keyboard, screen, apps) | DesktopAgent class | Both |


### Voice Pipeline

| File | Purpose | Active In |
|------|---------|-----------|
| voice/capture.py | Shared AudioCaptureService - single mic stream, fan-out to subscribers | Both |
| voice/devices.py | Audio device enumeration and selection | Both |
| voice/engine.py | VoiceEngine orchestrates wake-word frames, VAD recording, Whisper transcription | Both |
| voice/listener.py | Listener - faster-whisper STT + webrtcvad silence detection | Both |
| voice/pipeline.py | VoicePipeline reusable facade combining wake, listener, speaker | Both |
| voice/speaker.py | Speaker - Edge TTS with Piper fallback, pygame playback, barge-in | Both |
| voice/speech_service.py | SpeechOutputService wraps Speaker with state reporting | Both |
| voice/voice_state.py | VoiceState - single source of truth for GUI voice telemetry | Both |
| voice/wakeword.py | WakeWordEngine - openwakeword hey_jarvis offline detection | Both |
| voice/audio_log.py | Centralized audio logger to %%LOCALAPPDATA%%/JARVIS/logs/audio.log | Both |

## 2. COMPLETE CAPABILITY INVENTORY

See JARVIS_CAPABILITY_MATRIX.csv for the full structured inventory.

## 3. TEST AUDIT

### Test Files

| Test File | Tests | Uses Mocks | Real Windows | Source Only | Package | Real Mic | Real Mouse | Real Office | Real Browser |
|-----------|-------|-----------|-------------|-------------|---------|----------|------------|-------------|-------------|
| test_router.py | Fast-lane routing (40+ commands) | Yes | No | Yes | No | No | No | No | No |
| test_backend_regression.py | Open/close, folder resolution, planner, browser detection | Yes | No | Yes | No | No | No | No | No |
| test_llm.py | JSON extraction, error sanitization | Yes | No | Yes | No | No | No | No | No |
| test_gui.py | Window build, buttons, timelime, registry, voice toggle | Yes | No | Yes | No | No | No | No | No |
| test_integration.py | Config values, DesktopAgent, planner, news, GUI buttons | Yes | Clipboard | Yes | No | No | No | No | No |
| test_audio.py | VoiceState, device selection, capture service, packaged paths | Yes | No | Yes | No | No | No | No | No |
| test_controller.py | Controller bridge, voice start/stop, mute, shutdown | Yes | No | Yes | No | No | No | No | No |
| test_registry.py | Session registry close operations | Yes | No | Yes | No | No | No | No | No |
| test_registry_window.py | Registry fields, window control, office detection | Yes | No | Yes | No | No | No | No | No |
| test_settings.py | Settings load/save, defaults, unknown keys | Yes | No | Yes | No | No | No | No | No |
| test_voice.py | Speech cleanup, speaker fallback, CLI args | Yes | No | Yes | No | No | No | No | No |

### Test Totals
- **Total test files:** 11
- **Tests using mocks:** 47+ (all tests use mocks)
- **Tests using real integrations:** 1 (clipboard roundtrip test)
- **Tests performing real Windows actions:** 1 (clipboard)
- **Tests with real microphone/audio:** 0
- **Tests with real mouse/keyboard:** 0
- **Tests with real Office COM:** 0
- **Tests with real browser:** 0
- **Tests in packaged mode:** 0

## 4. PACKAGED BUILD AUDIT

### JARVIS-GUI.spec vs JARVIS.spec Differences

| Feature | JARVIS-GUI.spec (GUI build) | JARVIS.spec (console build) |
|---------|---------------------------|----------------------------|
| Entry point | desktop_main.py | main.py |
| Console | False (windowed) | True (console) |
| PySide6 | Included | EXCLUDED |
| gui modules | All included | Not included |
| EXE name | JARVIS | JARVIS |
| Output folder | dist/JARVIS/ | dist/JARVIS/ |

### Features Working in Source but Broken in Package

| Feature | Source | Package | Error |
|---------|--------|---------|-------|
| Browser (Playwright) | Works | BROKEN | PermissionError WinError 5 |
| Router (Qwen) | Works | BROKEN | torch circular import |
| Wake word | Works | BROKEN | sklearn resource missing |
| Edge TTS | Works then fails | Same | HTTP 403 (not package-specific) |
