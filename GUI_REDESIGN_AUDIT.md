# JARVIS Cinematic GUI Redesign Audit

Date: 2026-07-20

## Scope and Constraints

- Source root: `C:\Users\Burab\OneDrive\Desktop\JARVIS`
- GUI framework: PySide6
- Presentation-only redesign: backend command routing and business logic remain unchanged.
- Visual reference is used for composition, density, hierarchy, and atmosphere only.
- All graphics remain original and procedural; no character likeness, movie artwork, logos, fonts, or extracted image assets are used.
- Hermes remains disabled and is not installed in this phase.
- Unknown backend values render as `Unavailable`, `Disconnected`, `Waiting`, or `Not configured`.

## Existing Entry and Window

- GUI entry point: `desktop_main.py`
- Main window: `gui/main_window.py::MainWindow`
- Settings dialog: `gui/settings_window.py::SettingsWindow`
- System tray: `gui/tray.py::TrayIcon`
- Theme: `gui/styles.py::APP_QSS`
- Procedural center display: `gui/core_widget.py::ReactorCore`
- Capability page: `gui/capabilities_page.py::CapabilitiesPage`

The current window is a horizontal split between one reactor/telemetry column and one tabbed workspace. It is functional and responsive but does not match the requested dashboard density, three-column hierarchy, top subsystem rail, or bottom navigation composition.

## Existing Real State Sources

- `AssistantController.status_snapshot()` supplies voice state, controller state, session count, OpenRouter/Kimi availability, Hermes disabled state, browser state, Office state, memory, research, news, and real system metrics.
- `SessionRegistry.get_status()` supplies JARVIS-owned applications, folders, browser tabs, documents, process/window metadata, and ownership state.
- `LiveTask.snapshot()` supplies task ID, description, application, step, mode, progress, status, and task metadata.
- `CapabilityRegistry.report()` supplies dynamic capability count, health, permission, risk, connectivity, dependencies, timestamps, and details.
- `ControllerBridge` marshals backend callbacks to the GUI thread.

## Existing Signal Wiring

The controller currently exposes callbacks for:

- state
- status
- transcription
- response
- timeline
- registry
- log
- wakeword
- voicestate
- agentstatus
- capabilities
- taskstatus

`gui/workers.py::ControllerBridge` converts each callback to a Qt signal. Confirmation requests are also delivered through `confirmationRequested`, while the worker thread remains paused on a `threading.Event` until approve, deny, cancel, close, or timeout resolves the request.

## Worker Threads

- `GuiController` uses `QThreadPool` for typed commands, preload, capability scanning, speech, and GUI-triggered backend work.
- `AssistantController` owns the voice engine and its audio/wake-word threads.
- Live Word COM work uses the existing backend execution thread and dedicated COM handling.
- GUI widgets are updated only from Qt signal slots or GUI timers.

## Existing Animation

`ReactorCore` is an original `QPainter` visualization with layered arcs, state colors, a real microphone-level ring, and reduced-motion support. Its timer is state-sensitive: active states update faster, while idle uses a slower cadence.

## Existing Assets and Packaging

- `jarvis.ico` and `icon_preview.png` are packaged.
- `gui/` is included as PyInstaller data and modules are explicitly hidden-imported.
- No cinematic textures or external artwork are required by the redesign.
- `JARVIS-GUI.spec` currently includes `.env`; this is a release-safety defect and must be removed before packaging.

## Missing Presentation Components

- Three-column dashboard with independently scrollable dense panels
- Real subsystem status rail
- Date/time HUD
- Dedicated conversation, task, reasoning-summary, Hermes, system gauge, timeline, applications, Office, browser, research, quick-action, memory, automation, logs, and settings pages
- Search/filter/detail controls on the capability page
- Responsive 1080p composition
- Explicit reduced-motion stylesheet and persistent theme choice
- Original neural/AI core composition tied to execution state

## Backend Signal Gaps

Some requested semantic signals do not exist as separate backend callbacks. They can be derived safely in the GUI from existing authoritative signals:

- microphone level from `voicestate.input_level`
- planner/execution/confirmation phase from `state`, `agentstatus`, and `timeline`
- speech phase from `voicestate.speaker_state`
- application opened/focused/closed from registry snapshot deltas
- Office/browser/research state from status and live-task snapshots
- audit event from timeline/log callbacks

No synthetic success state or random metric is needed.

## Layout Constraints

- Minimum usable target: 1920x1080 with scaling-aware layouts.
- Smaller windows must remain operable through scroll areas rather than clipped fixed geometry.
- All high-density panel text must remain selectable/readable.
- Expensive discovery and health checks must remain off the GUI thread.
- Live preview remains unavailable unless the backend supplies a safe event-driven preview; continuous desktop capture is prohibited.

## Implementation Decision

Retain `MainWindow`, `GuiController`, controller callbacks, settings dialog, tray, and backend service APIs. Recompose `MainWindow` around reusable widgets and add presentation pages. Keep compatibility attributes used by existing tests and integrations. Extend bridge signals only as aliases derived from existing backend events; do not replace backend callbacks or command routing.
