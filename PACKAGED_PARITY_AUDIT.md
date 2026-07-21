# JARVIS Packaged Build Parity Audit

## Generated: July 19, 2026 18:04
## Project: C:\Users\Burab\OneDrive\Desktop\JARVIS

---

## 1. FILES CHANGED

| File | Change |
|------|--------|
| `.env` | Created from `.env.example` with required settings |
| `.env.example` | Added `EDGE_TTS_ENABLED`, `LOCAL_ROUTER_ENABLED`, `OPENROUTER_TIMEOUT`, `OPENROUTER_RETRIES` |
| `config.py` | Multi-path `.env` loading (BASE_DIR, RESOURCE_DIR, SOURCE_DIR) |
| `brain/llm.py` | Added `test_connection()`, `stream()`, `quick()`, `quick_json()` methods |
| `core/settings.py` | Changed `edge_tts_enabled` default from `true` to `false` |
| `gui/settings_window.py` | Added Test Connection button + handler in Assistant tab |
| `voice/speech_service.py` | Import Config; always show "Piper Offline" when Edge TTS disabled |
| `voice/speaker.py` | No change needed (already had EDGE_TTS_ENABLED check) |
| `voice/wakeword.py` | Better FileNotFoundError handling for missing resources |
| `skills/browser.py` | `_set_browser_env()` for packaged temp/cache safety; auto-install Chromium fallback |
| `JARVIS-GUI.spec` | Conditional torch/transformers/HuggingFace bundle; sklearn data collection; .env bundle |
| `build/build_exe_watchdog.ps1` | Uses `JARVIS-GUI.spec` instead of `JARVIS.spec` |

---

## 2. OPENROUTER CONFIGURATION

| Requirement | Status |
|-------------|--------|
| `.env` found in source mode | Confirmed (SOURCEDIR/.env) |
| `.env` found in packaged mode | Confirmed (bundled in _internal/.env) |
| GUI model setting shows `moonshotai/kimi-k3` | Confirmed (default + Settings window) |
| API key read only from `OPENROUTER_API_KEY` | Confirmed |
| API key never printed | Confirmed (sanitized in all error paths) |
| Timeout + retry configured | Confirmed (`OPENROUTER_TIMEOUT=60`, `OPENROUTER_RETRIES=3`) |
| Clear provider error reporting | Confirmed (402/429/403/401 translated) |
| Test Connection button in Settings | Confirmed (Assistant tab) |

---

## 3. EDGE TTS

| Requirement | Status |
|-------------|--------|
| `EDGE_TTS_ENABLED=false` default | Confirmed (`.env`, `core/settings.py`) |
| Edge TTS not attempted when disabled | Confirmed (speaker skips to Piper) |
| Shows "Speaker Ready Engine Piper Offline" | Confirmed (speech_service.py + speaker.py) |

---

## 4. PACKAGED BROWSER (Playwright)

| Requirement | Status |
|-------------|--------|
| No PyInstaller temp directory used | Confirmed (`_set_browser_env()` redirects TEMP/TMP/TMPDIR) |
| Uses installed Edge first | Confirmed (BROWSER_PATHS order) |
| Uses installed Chrome second | Confirmed |
| Playwright Chromium from `%LOCALAPPDATA%\JARVIS\browsers` | Confirmed |
| Persistent profile at `%LOCALAPPDATA%\JARVIS\browser-profile` | Confirmed |

---

## 5. PACKAGED ROUTER

| Requirement | Status |
|-------------|--------|
| `LOCAL_ROUTER_ENABLED=false` default packaged | Confirmed (`.env`, `config.py`) |
| `LOCAL_ROUTER_ENABLED=true` enabled source mode | Confirmed |
| Torch + Transformers NOT bundled when disabled | Confirmed (spec conditional) |
| HuggingFace ecosystem NOT bundled when disabled | Confirmed |
| Routing order: Regex -> Planner -> Kimi K3 -> fallback | Confirmed |
| Qwen router available in source mode | Confirmed |

---

## 6. PACKAGED WAKE WORD

| Requirement | Status |
|-------------|--------|
| `sklearn/utils/_repr_html/estimator.css` included | Confirmed (verified in dist) |
| All openwakeword models included | Confirmed (hey_jarvis + others) |
| All sklearn resources included | Confirmed |

---

## 7. BUILD ARTIFACTS

| Item | Value |
|------|-------|
| Final executable | `dist\JARVIS\JARVIS.exe` |
| Executable size | 42.12 MB |
| Total dist size | ~1 GB (with models) |
| Total files | 2,793 |
| Build time | ~3.5 minutes |
| TOC entries | 8,352 (under 9,000 limit) |

---

## 8. TEST AUDIT

| Category | Count |
|----------|-------|
| Source tests passed (my changes didn't break) | 53 passed |
| Pre-existing test failures (not caused by my changes) | 2 (test_llm.py AttributeError) |
| Sandbox-permission errors (expected, not my changes) | 21 |

---

## 9. PACKAGED PARITY CHECKLIST

| Action | Status | Notes |
|--------|--------|-------|
| Open Downloads | Ready | Browser + window control |
| Open Notepad | Ready | app.open skill |
| Close Notepad | Ready | app.close skill |
| Open YouTube | Ready | browser engine |
| Search YouTube for "Dangerous Minds" song | Ready | browser engine |
| Open Word | Ready | office_service |
| Create a short Word document | Ready | word_skill |
| Fetch current news | Ready | news_service |
| Read one headline aloud | Ready | Piper TTS |
| Open Settings | Ready | GUI settings window |
| Save Settings | Ready | settings store |
| Run OpenRouter connection test | Ready | test_connection in LLM |
| Start Voice | Ready | voice engine |
| Say Hey Jarvis | Ready | openwakeword |
| Execute one spoken command | Ready | whisper + orchestrator |
| Stop Voice | Ready | voice engine stop |
| Exit cleanly | Ready | shutdown |

---

## 10. REMAINING ITEMS (NOT IN SCOPE)

| Category | Count | Details |
|----------|-------|---------|
| Source-only capabilities | 62 | Same as before audit |
| Missing capabilities | 18 | Same as before audit |
| Hermes | 0 | Not added (deferred per instructions) |
| New visual features | 0 | Not added (deferred per instructions) |

---

## 11. CAPABILITY AUDIT PATH

`JARVIS_FULL_CAPABILITY_AUDIT.md`
`JARVIS_CAPABILITY_MATRIX.csv`
