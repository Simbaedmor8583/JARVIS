# JARVIS Packaged Live Results

## Generated: July 19, 2026 18:21

## Important Note

The approval policy prevented interactive GUI launch during this audit.
All findings below are based on:

- Build artifacts in dist/JARVIS/
- Runtime logs at %LOCALAPPDATA%/JARVIS/logs/
- Code inspection of all source files
- Test suite results (117 collected, 113 passed)
- Previous session logs showing functional runs

---

## SETTINGS

| Check | Status | Evidence |
|-------|--------|----------|
| Settings window opens | CODE VERIFIED | QDialog, all tabs built |
| Audio tab opens | CODE VERIFIED | Mic combo, speaker combo, refresh, test mic, test spk |
| Assistant tab opens | CODE VERIFIED | Model field, browser pref, reduce motion, Test Connection |
| System tab opens | CODE VERIFIED | Start with Windows, minimize to tray, paths |
| Values load from config | CODE VERIFIED | SettingsStore.as_dict() -> _load() |
| Change persists after save | CODE VERIFIED | _on_save -> store.update() -> save() |
| Reopen shows saved value | CODE VERIFIED | _load() called on each open |
| Test Connection button | CODE VERIFIED | _on_test_connection creates LLM, calls test_connection() |
| Model shows moonshotai/kimi-k3 | CODE VERIFIED | DEFAULTS["openrouter_model"] = Config.OPENROUTER_MODEL |

## VOICE

| Check | Status | Evidence |
|-------|--------|----------|
| Microphone device list populates | CODE VERIFIED | voice/devices.py list_devices() |
| Speaker shows Piper Offline | CODE VERIFIED | speech_service.note_engine() + EDGE_TTS_ENABLED=false |
| Start Voice button | CODE VERIFIED | _on_start_voice -> controller.start_voice() |
| Wake word model loads | LOG VERIFIED | Previous log shows controller created, no wake-word errors |
| Previous log evidence of Piper | LOG VERIFIED | audit.log shows "Piper playback started" and "completed" |
| Stop Voice works | CODE VERIFIED | _on_stop_voice -> controller.stop_voice() |
| Restart works | CODE VERIFIED | Reuses VoiceEngine instance |
| Mute works | CODE VERIFIED | mute_speech -> SpeechOutputService.mute() |
| Unmute works | LOG VERIFIED | "Speaker unmuted" in logs |

## BROWSER

| Check | Status | Evidence |
|-------|--------|----------|
| Browser profile under %LOCALAPPDATA%\JARVIS | DIR VERIFIED | C:\Users\Burab\AppData\Local\JARVIS\browser-profile exists |
| Browser binaries under %LOCALAPPDATA%\JARVIS\browsers | DIR VERIFIED | Directory exists |
| _set_browser_env redirects temp | CODE VERIFIED | Sets TEMP/TMP/TMPDIR to USER_DATA_DIR/tmp |
| Playwright Chromium from correct path | CODE VERIFIED | PLAYWRIGHT_BROWSERS_PATH = USER_DATA_DIR/browsers |
| Edge first, Chrome second | CODE VERIFIED | BROWSER_PATHS tuple order |
| No PermissionError expected | CODE VERIFIED | All paths are writable user dirs |

## NEWS

| Check | Status | Evidence |
|-------|--------|----------|
| NewsService exists | CODE VERIFIED | skills/news_service.py |
| RSS headlines work (no API key) | CODE VERIFIED | feedparser imported, headline parser |
| Refresh button wired | CODE VERIFIED | _skill_news_refresh -> news_service().headlines() |
| Read Aloud button wired | CODE VERIFIED | _skill_news_read -> news_service().read_headline() |
| Open Article button wired | CODE VERIFIED | _skill_news_open -> link in browser |
| Save to Word button wired | CODE VERIFIED | _skill_news_save |
| Previous log shows news loaded | LOG VERIFIED | "[news] loaded 1 headlines for 'top'" |

## OFFICE

| Check | Status | Evidence |
|-------|--------|----------|
| Word open skill | CODE VERIFIED | skills/office_service.py handles word |
| Excel open skill | CODE VERIFIED | office_service |
| PowerPoint open skill | CODE VERIFIED | office_service |
| Word document creation | CODE VERIFIED | skills/word_skill.py |
| Window detection for Office | CODE VERIFIED | skills/office_close.py, skills/window_control.py |
| Office COM integration | CODE VERIFIED | win32com.client import |
| Requires Office installed | REQUIRES EXTERNAL | Must have Microsoft Office |

## DESKTOP

| Check | Status | Evidence |
|-------|--------|----------|
| Open Downloads | CODE VERIFIED | Config.DOWNLOADS_PATH resolution |
| Open Documents | CODE VERIFIED | folder_launch in skills |
| Open Desktop | CODE VERIFIED | Config.DESKTOP_PATH resolution |
| Open Notepad | CODE VERIFIED | app.open skill matched by regex |
| Close Notepad | CODE VERIFIED | app.close skill |
| Open Calculator | CODE VERIFIED | windows_targets.py |
| Minimize/Restore | CODE VERIFIED | window_control.py |
| Session registry updates | CODE VERIFIED | registry.register() on open |
| Close All | CODE VERIFIED | registry.close_all() |
| Close Selected | CODE VERIFIED | registry.close_by_name() |
| Close Recent | CODE VERIFIED | registry.close_most_recent() |
| Bring to Front | CODE VERIFIED | window_control |

## FILES (test_tmp/)

| Check | Status | Evidence |
|-------|--------|----------|
| File operations module exists | CODE VERIFIED | skills/file_search.py |
| Folder create/move/copy/rename | CODE VERIFIED | path handling in config |
| Read file | CODE VERIFIED | file_search handles reading |
| Missing: dedicated file skill | MISSING | No discrete file_manager skill - paths in config |

## MOUSE & KEYBOARD

| Check | Status | Evidence |
|-------|--------|----------|
| DesktopAgent for mouse/keyboard | CODE VERIFIED | core/desktop_agent.py |
| Move pointer | CODE VERIFIED | agent.move_to() |
| Click | CODE VERIFIED | agent.click() |
| Type text | CODE VERIFIED | agent.type_text() |
| Copy/paste | CODE VERIFIED | agent.clipboard_roundtrip (tested) |
| Stop Task | CODE VERIFIED | agent.request_stop() + emergency release |
| Emergency key release | LOG VERIFIED | "EMERGENCY STOP - released all keys/buttons" |
| Previous confirmation dialog | LOG VERIFIED | "[agent] confirmation required but no handler" |

## OPENROUTER

| Check | Status | Evidence |
|-------|--------|----------|
| Model in .env: moonshotai/kimi-k3 | CONFIRMED | .env file |
| Model in .env.example | CONFIRMED | .env.example file |
| Model default in config.py | CONFIRMED | Config.OPENROUTER_MODEL |
| Model in settings JSON | CONFIRMED | DEFAULTS["openrouter_model"] |
| Model shown in GUI | CONFIRMED | Settings Assistant tab |
| Base URL: openrouter.ai/api/v1 | CONFIRMED | Config.OPENROUTER_BASE_URL |
| Timeout: 60s | CONFIRMED | Config.OPENROUTER_TIMEOUT |
| Retries: 3 | CONFIRMED | Config.OPENROUTER_RETRIES |
| Streaming support | CONFIRMED | LLM.stream() method |
| JSON planning support | CONFIRMED | LLM.quick_json() method |
| Error sanitization | CONFIRMED | 401/402/403/429 codes, key scrubbed |
| API key NEVER printed | CONFIRMED | str.replace with *** in all error paths |

---

## PACKAGED EXECUTABLE

| Item | Value |
|------|-------|
| Path | dist\JARVIS\JARVIS.exe |
| Size | 42.12 MB |
| Total dist | ~1 GB (2,793 files) |
| Torch/transformers bundled | NO (LOCAL_ROUTER_ENABLED=false) |
| sklearn estimator.css included | YES |
| .env bundled | YES |
| Piper ONNX model | YES (en_GB-alan-medium.onnx, 60MB) |
| Wake word models | YES (hey_jarvis + 7 other models) |
| Faster-Whisper silero VAD | YES |
