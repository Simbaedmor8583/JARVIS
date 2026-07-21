# JARVIS Second Capability Audit

## Generated: July 19, 2026 18:23

---

## HOW TO READ STATUSES

- WORKING AND LIVE VERIFIED ? confirmed running in a live session
- WORKING IN SOURCE ONLY ? works with `py -3.12` but not packaged
- WORKING IN PACKAGED BUILD ? verified in dist/JARVIS/JARVIS.exe
- CONNECTED BUT NOT LIVE VERIFIED ? code paths exist, wiring complete, but not launched
- PARTIALLY WORKING ? works in some contexts, fails in others
- GUI ONLY ? GUI button exists but backend not wired or not tested
- BACKEND ONLY ? code exists but no GUI button or workflow
- TEST ONLY ? unit test passes but no real integration
- BROKEN ? confirmed failure in any mode
- MISSING ? no code exists for this feature
- DISABLED ? deliberately turned off
- REQUIRES CONFIGURATION ? needs API key or env var
- REQUIRES LOGIN ? needs browser auth
- REQUIRES EXTERNAL SOFTWARE ? needs installed app
- REQUIRES ADMINISTRATOR ACCESS ? needs elevation
- UNSAFE TO TEST AUTOMATICALLY ? destructive or dangerous

---

## COMPLETE CAPABILITY INVENTORY

### SYSTEM: Core Infrastructure

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Config loading (.env) | config.py | N/A | N/A | N/A | YES | WORKING IN PACKAGED BUILD |
| Settings store (config.json) | core/settings.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Settings window | gui/settings_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Save settings | core/settings.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Multi-path .env loading | config.py | N/A | N/A | N/A | YES | WORKING IN PACKAGED BUILD |
| Directory creation (ensure_dirs) | config.py | N/A | N/A | N/A | YES | WORKING IN PACKAGED BUILD |

### SYSTEM: OpenRouter Cloud Brain

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| LLM.chat() | brain/llm.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| LLM.stream() | brain/llm.py | YES | NO | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| LLM.quick() | brain/llm.py | YES | NO | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| LLM.quick_json() | brain/llm.py | NO | NO | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| LLM.test_connection() | brain/llm.py | YES | NO | NO | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Error sanitization (key scrubbing) | brain/llm.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Timeout + retry | brain/llm.py | N/A | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Test Connection button | gui/settings_window.py | YES | NO | NO | YES | CONNECTED BUT NOT LIVE VERIFIED |

### SYSTEM: Local Router

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Qwen router classify() | brain/router.py | NO | YES | YES | DISABLED | DISABLED |
| Qwen router preload() | brain/router.py | NO | NO | NO | DISABLED | DISABLED |
| Fast lane regex routing | brain/router.py | YES | YES | YES | YES | WORKING IN PACKAGED BUILD |
| Valid skills allowlist | brain/router.py | N/A | N/A | N/A | YES | WORKING IN PACKAGED BUILD |

### SYSTEM: Planner

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Multi-step plan command | core/planner.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Compound command decomposition | core/planner.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Planner validate allowlist | core/planner.py | N/A | N/A | N/A | YES | TEST ONLY |

### SYSTEM: DesktopAgent

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Mouse movement | core/desktop_agent.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Mouse click | core/desktop_agent.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Keyboard typing | core/desktop_agent.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Copy/paste clipboard | core/desktop_agent.py | YES | YES | YES | YES | TEST ONLY (clipboard test passes) |
| Screenshot | core/desktop_agent.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Active window title | core/desktop_agent.py | YES | NO | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Emergency stop | core/desktop_agent.py | YES | YES | YES | YES | WORKING IN PACKAGED BUILD |
| Confirmation system | core/desktop_agent.py | NO | NO | NO | YES | PARTIALLY WORKING |
| Stop Task button | gui/main_window.py | YES | NO | NO | YES | CONNECTED BUT NOT LIVE VERIFIED |

### SESSION: Registry

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Register opened item | core/registry.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Close by name | core/registry.py | YES | YES | YES | YES | TEST ONLY |
| Close all | core/registry.py | YES | YES | YES | YES | TEST ONLY |
| Close most recent | core/registry.py | YES | YES | YES | YES | TEST ONLY |
| Registry panel in GUI | gui/main_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Close Selected button | gui/main_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Close Recent button | gui/main_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Close All button | gui/main_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Bring to Front button | gui/main_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |

### VOICE: Microphone

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Device enumeration | voice/devices.py | YES | YES | NO | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Microphone selection | voice/devices.py | YES | YES | NO | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Test Microphone (3s recording) | gui/settings_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |
| AudioCaptureService | voice/capture.py | NO | YES | NO | YES | WORKING IN SOURCE ONLY |
| Input level meter | gui/settings_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |

### VOICE: Wake Word

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| hey_jarvis detection | voice/wakeword.py | NO | YES | NO | YES | WORKING IN PACKAGED BUILD |
| Wake word score display | voice/voice_state.py | YES | YES | NO | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Wake word threshold config | config.py | YES | YES | NO | YES | CONNECTED BUT NOT LIVE VERIFIED |
| sklearn estimator.css bundled | JARVIS-GUI.spec | N/A | N/A | N/A | YES | WORKING IN PACKAGED BUILD |

### VOICE: Speech Recognition

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Whisper model (faster-whisper) | voice/listener.py | NO | YES | NO | YES | CONNECTED BUT NOT LIVE VERIFIED |
| VAD silence detection | voice/listener.py | NO | YES | NO | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Whisper model selection | config.py | YES | YES | NO | YES | CONNECTED BUT NOT LIVE VERIFIED |

### VOICE: Speech Output

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Piper TTS (offline) | voice/speaker.py | YES | YES | NO | YES | WORKING IN PACKAGED BUILD |
| Edge TTS (disabled) | voice/speaker.py | N/A | N/A | N/A | DISABLED | DISABLED |
| Test Speaker (Piper) | gui/settings_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Barge-in (Jarvis stop) | voice/speaker.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Voice mute/unmute | voice/speech_service.py | YES | YES | NO | YES | WORKING IN PACKAGED BUILD |
| Speech state reporting | voice/voice_state.py | YES | YES | NO | YES | CONNECTED BUT NOT LIVE VERIFIED |

### BROWSER

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Open browser (launch_persistent_context) | skills/browser.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Open YouTube | skills/browser.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| YouTube search | skills/browser.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Open known sites (KNOWED_SITES) | skills/browser.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Google search | skills/browser.py | NO | NO | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Close browser tab | skills/browser.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Close browser | skills/browser.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Persistent profile | skills/browser.py | N/A | N/A | N/A | YES | WORKING IN PACKAGED BUILD |
| Auto-install Chromium | skills/browser.py | N/A | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Open Browser button | gui/main_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |
| YouTube Search button | gui/main_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |

### DESKTOP: Window Control

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Open application | skills/window_control.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Close application | skills/window_control.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Minimize window | skills/window_control.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Bring to front | skills/window_control.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Open Downloads | main.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Open Documents | main.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Open Notepad | skills/window_control.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Close Notepad | skills/window_control.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Open Calculator | skills/window_control.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Open Files button | gui/main_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Open Logs button | gui/main_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |

### SYSTEM: Volume & Media

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Volume up/down | skills/volume.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Mute/unmute system | skills/volume.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Media play/pause/next/stop | skills/media.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Play music (YouTube) | skills/media.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |

### SYSTEM: Power & Status

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Screenshot | core/desktop_agent.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Screenshot button | gui/main_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Lock PC | skills/system_control.py | NO | YES | YES | YES | UNSAFE TO TEST AUTOMATICALLY |
| Shutdown | skills/system_control.py | NO | YES | YES | YES | UNSAFE TO TEST AUTOMATICALLY |
| Restart | skills/system_control.py | NO | YES | YES | YES | UNSAFE TO TEST AUTOMATICALLY |
| Sleep | skills/system_control.py | NO | YES | YES | YES | UNSAFE TO TEST AUTOMATICALLY |
| Battery status | skills/system_control.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Read Screen button | gui/main_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |
| System status chip | gui/main_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |

### OFFICE

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Open Word | skills/office_service.py | NO | YES | YES | YES | REQUIRES EXTERNAL SOFTWARE |
| Create Word document | skills/word_skill.py | YES | YES | YES | YES | REQUIRES EXTERNAL SOFTWARE |
| Open Excel | skills/office_service.py | NO | YES | YES | YES | REQUIRES EXTERNAL SOFTWARE |
| Open PowerPoint | skills/office_service.py | NO | YES | YES | YES | REQUIRES EXTERNAL SOFTWARE |
| Create PPT slide | skills/ppt_skill.py | NO | YES | YES | YES | REQUIRES EXTERNAL SOFTWARE |
| Close Office apps | skills/office_close.py | NO | YES | YES | YES | REQUIRES EXTERNAL SOFTWARE |
| Word Report button | gui/main_window.py | YES | N/A | N/A | YES | REQUIRES EXTERNAL SOFTWARE |
| Office COM dependency | requirements.txt | N/A | N/A | N/A | YES | REQUIRES EXTERNAL SOFTWARE |

### NEWS

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| RSS feed parsing | skills/news_service.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| NewsAPI optional | skills/news_service.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Refresh headlines | gui/main_window.py | YES | NO | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Read headline aloud | gui/main_window.py | YES | NO | NO | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Open article | gui/main_window.py | YES | NO | NO | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Save to Word | gui/main_window.py | YES | NO | NO | YES | CONNECTED BUT NOT LIVE VERIFIED |
| News cache (15 min) | skills/news_service.py | N/A | N/A | N/A | YES | WORKING IN PACKAGED BUILD |

### RESEARCH

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Web research | skills/research.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Multi-turn research | skills/research.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Research save | skills/research.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |

### ORGANIZER

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Desktop organizer | skills/organizer.py | YES | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Organize Desktop button | gui/main_window.py | YES | N/A | N/A | YES | CONNECTED BUT NOT LIVE VERIFIED |

### EMAIL

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| SMTP/IMAP (Gmail) | skills/emailer.py | NO | YES | YES | YES | REQUIRES CONFIGURATION |
| Browser Gmail mode | skills/gmail.py | NO | YES | YES | YES | REQUIRES LOGIN |
| Send email | skills/emailer.py | NO | YES | YES | YES | REQUIRES CONFIGURATION |
| Check inbox | skills/gmail.py | NO | YES | YES | YES | REQUIRES LOGIN |

### MUSIC

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Play music (YouTube) | skills/media.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| YouTube search (music) | skills/youtube_music.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Media controls (pause/resume/skip) | skills/media.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |

### WHATSAPP

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| WhatsApp Web | skills/whatsapp.py | NO | YES | YES | YES | REQUIRES LOGIN |
| Auto-send mode | config.py | N/A | N/A | N/A | YES | REQUIRES LOGIN |

### FILE OPERATIONS

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| File search | skills/file_search.py | NO | YES | YES | YES | PARTIALLY WORKING |
| Create folder | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |
| Create file | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |
| Rename file | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |
| Copy file | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |
| Move file | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |
| Read file content | skills/file_search.py | NO | YES | YES | YES | PARTIALLY WORKING |
| Delete to trash | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |

### SCREEN UNDERSTANDING

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Read active window title | core/desktop_agent.py | YES | NO | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Screen OCR/text reading | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |
| Visual understanding | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |

### CHAT / CONVERSATION

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Chat (OpenRouter) | skills/chat.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Time/date queries | brain/router.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| Greeting on startup | desktop_main.py | NO | NO | NO | YES | CONNECTED BUT NOT LIVE VERIFIED |

### EXCEL SKILL

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Excel workbook creation | skills/excel_skill.py | NO | YES | YES | YES | REQUIRES EXTERNAL SOFTWARE |

### MEMORY

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Memory (JSON file) | skills/memory_skill.py | NO | YES | YES | YES | CONNECTED BUT NOT LIVE VERIFIED |
| memory.json path | config.py | N/A | N/A | N/A | YES | WORKING IN PACKAGED BUILD |

### AUDIT LOGGING

| Capability | Source File | GUI Wired | Voice Wired | Type Wired | Packaged | Status |
|------------|-------------|-----------|-------------|------------|----------|--------|
| Audio log | voice/audio_log.py | NO | YES | NO | YES | WORKING IN PACKAGED BUILD |
| Startup log | voice/audio_log.py | NO | NO | NO | YES | WORKING IN PACKAGED BUILD |
| Error log | voice/audio_log.py | NO | NO | NO | YES | WORKING IN PACKAGED BUILD |
| Command log | voice/audio_log.py | NO | YES | YES | YES | WORKING IN PACKAGED BUILD |

---

## SUMMARY COUNTS

| Status | Count |
|--------|-------|
| WORKING AND LIVE VERIFIED | ~19 |
| WORKING IN PACKAGED BUILD | ~15 |
| CONNECTED BUT NOT LIVE VERIFIED | ~42 |
| WORKING IN SOURCE ONLY | ~1 |
| TEST ONLY | ~3 |
| PARTIALLY WORKING | ~3 |
| BROKEN | 0 |
| MISSING | ~9 |
| DISABLED | ~3 |
| REQUIRES CONFIGURATION | ~3 |
| REQUIRES LOGIN | ~3 |
| REQUIRES EXTERNAL SOFTWARE | ~10 |
| UNSAFE TO TEST AUTOMATICALLY | ~4 |
| **TOTAL CAPABILITIES** | **~99** |
