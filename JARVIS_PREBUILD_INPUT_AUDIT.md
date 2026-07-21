# JARVIS Prebuild Input Audit

Date: 2026-07-20

## Source Tree

- Working source: `C:\Users\Burab\OneDrive\Desktop\JARVIS`
- Entry script: `desktop_main.py`
- Spec: `JARVIS-GUI.spec`
- Build command: `py -3.12 -m PyInstaller --noconfirm --clean JARVIS-GUI.spec`
- Spec uses the current working directory through PyInstaller `Analysis`; it does not reference another project copy, prior release, or old build tree.

## Data Inputs

- `data/piper` → `data/piper`
- `.env.example` → release root
- `jarvis.ico` → release root
- `icon_preview.png` → release root
- Piper `espeak-ng-data` → `piper/espeak-ng-data`
- `gui/themes` → `gui/themes`
- Package metadata and runtime data collected by PyInstaller hooks for setuptools, scikit-learn, openwakeword, faster-whisper, Playwright, PySide6, Edge TTS, and Piper.

`.env` was removed from the spec and must not appear in `dist` or `release`.

## Python Packages

- Project: `core`, `brain`, `voice`, `skills`, `gui`, `memory`, `utils`
- Dynamic skill discovery: every `skills` submodule is an explicit hidden import.
- GUI additions: dashboard, capabilities, secondary pages, HUD widgets, AI core, and dashboard panels are explicit hidden imports.
- Safety/runtime additions: capability registry/health, action manager, application/session registry, command cleanup, live task, planner, save workflow, and Windows controller are explicit hidden imports.

## Native and Optional Inputs

- Piper executable is included only when present in the Python 3.12 Scripts directory.
- NumPy and SciPy dynamic libraries are collected.
- Playwright, Qt, openwakeword, faster-whisper, Edge TTS, and Piper hook outputs are collected.
- Torch/Transformers and related Hugging Face packages remain excluded unless `LOCAL_ROUTER_ENABLED` is explicitly enabled at build time.

## Writable Runtime Data

Frozen runtime data resolves through `config.py` to `%LOCALAPPDATA%\JARVIS`. Configuration, logs, cache/temp, browser profile, and user session data are not read from the PyInstaller bundle.

## Excluded Private Inputs

- `.env`, API keys, passwords, cookies, browser profiles, personal documents, personal audit history, screenshots, `.test_tmp`, tests, and `.backups` are not spec data inputs.
