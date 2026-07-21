# GUI Architecture

## Runtime Layers

- `desktop_main.py`: creates QApplication, shows the window, then starts preload and capability health in a worker.
- `gui/workers.py`: thread-pool execution and Qt signal bridge.
- `core/assistant_controller.py`: shared typed/voice backend controller.
- `gui/main_window.py`: operational dashboard and user controls.
- `gui/core_widget.py`: state-driven AI core.
- `gui/capabilities_page.py`: searchable capability table.

## Operational Views

- Assistant: transcript, cleaned command, structured action, selected skill, response, active task, application, mode, step, progress, and task controls.
- Applications: current JARVIS-owned session registry.
- Skills: real backend commands only.
- News: real cached/fetched news state.
- Timeline: timestamped backend stages, validated actions, confirmation events, and execution results.
- System: live CPU, RAM, disk, network, temperature availability, GPU availability, and Python threads.
- Capabilities: dynamic registry status, permission, dependencies, health, and detail.

## Animation

The core receives real controller states: idle, listening, recording, processing, executing, speaking, ready, failure, and recovery. Voice amplitude comes from `VoiceState.input_level`. Reduced-motion mode disables rotation and lowers update cadence.

No random demo data is generated. Unsupported data displays `Unavailable`, `Disconnected`, `Waiting`, or `Disabled`.

## Current Boundaries

The preserved GUI does not yet implement dockable/floating panels, six color themes, or a full interactive planner graph. Hermes panels remain disabled because Hermes was intentionally not installed.

