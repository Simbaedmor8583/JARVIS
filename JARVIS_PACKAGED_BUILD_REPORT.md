# JARVIS Packaged Build Report

Date: 2026-07-20

## Build Input

- Source root: `C:\Users\Burab\OneDrive\Desktop\JARVIS`
- Entry point: `desktop_main.py`
- Spec: `JARVIS-GUI.spec`
- Command: `py -3.12 -m PyInstaller --noconfirm --clean JARVIS-GUI.spec`
- Output mode: windowed onedir
- Hermes included: no

`JARVIS-GUI.spec` analyzed the current source root and did not reference another project copy or an old release. Cinematic QSS resources, GUI modules, confirmation/action services, capability registry, voice, browser, Office, and packaged runtime dependencies were included. `.env`, logs, screenshots, test output, personal browser data, and audit history were not included.

## Pre-Build Validation

- Python compile: passed.
- Focused audio tests: 17 passed.
- Tests collected: 250.
- Tests passed: 250.
- Tests failed: 0.
- Tests skipped: 0.
- Warning: one third-party `webrtcvad/pkg_resources` deprecation warning.

## Release

- Executable: `release\JARVIS-GUI\JARVIS.exe`
- Executable SHA-256: `7210C318BF0EDA12ECEEEBDB0896C0C63E3C5FF733ADF1ACC439F20C95192235`
- Release bytes: 1,077,123,602.
- Release files: 2,780.
- Full manifest: `JARVIS_RELEASE_MANIFEST.txt`.
- Previous release backup: `release\backups\JARVIS-GUI-before-desktop-web-adapters-20260720-063138`.
- GUI source backup: `.backups\gui_before_cinematic_redesign`.

## Source Changes Included

### Cinematic GUI

- `desktop_main.py`
- `gui\main_window.py`
- `gui\dashboard_page.py`
- `gui\capabilities_page.py`
- `gui\secondary_pages.py`
- `gui\settings_window.py`
- `gui\styles.py`
- `gui\workers.py`
- `gui\widgets\__init__.py`
- `gui\widgets\ai_core_widget.py`
- `gui\widgets\dashboard_panels.py`
- `gui\widgets\hud.py`
- `gui\themes\cinematic.qss`
- `gui\themes\reduced_motion.qss`

### Backend/Packaging Corrections

- `config.py`
- `core\assistant_controller.py`
- `core\automation_intents.py`
- `core\ui_automation.py`
- `core\registry.py`
- `core\save_workflow.py`
- `core\settings.py`
- `main.py`
- `skills\browser.py`
- `skills\desktop_automation.py`
- `skills\web_automation.py`
- `skills\website_adapters.py`
- `voice\engine.py`
- `voice\listener.py`
- `voice\speaker.py`
- `voice\wakeword.py`
- `brain\router.py`
- `JARVIS-GUI.spec`

### Tests

- `tests\test_cinematic_gui.py`
- `tests\test_save_workflow.py`
- `tests\test_voice.py`
- `tests\test_audio.py`
- `tests\test_automation_intents.py`
- `tests\test_desktop_automation.py`
- `tests\test_ui_automation.py`
- `tests\test_web_automation.py`
- `tests\test_windows_routing.py`

### Armored Sentinel Update

- `gui\widgets\ai_core_widget.py`
- `tests\test_cinematic_gui.py`
- Backup: `.backups\robot_before_armored_sentinel\ai_core_widget.py`

## Build Notes

- PyInstaller reported optional missing modules such as `dask`, `nvcuda.dll`, and selected scikit-learn helper modules. These were not used by the validated JARVIS paths and did not prevent build or runtime validation.
- The packaged save alias now resolves to `%LOCALAPPDATA%\JARVIS\temp`, not `_internal`.
- The exact required live-Word phrase initially exposed an app-open fallback. A minimal fast-lane route and regression test corrected it before the final rebuild.
- The packaged skip-preload voice path now initializes WebRTC VAD before recording; acoustic validation reached a 0.97 wake score and completed transcription and routing.

Build status: **SUCCESS**. Release readiness remains **NOT READY** only because human-spoken packaged validation is outstanding.
