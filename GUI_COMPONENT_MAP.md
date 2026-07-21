# JARVIS GUI Component Map

Date: 2026-07-20

## Window Composition

- `gui/main_window.py`: title rail, real subsystem rail, page stack, bottom navigation, compatibility aliases, state slots, and GUI action forwarding.
- `gui/dashboard_page.py`: responsive three-column dashboard with independently scrollable high-density columns.
- `gui/capabilities_page.py`: dynamic registry search, category/status/permission/risk filters, capability table, details, and health test.
- `gui/secondary_pages.py`: Tasks, Memory, Research/News, Automation, Logs, and Settings pages.

## Reusable Widgets

- `gui/widgets/hud.py`: `HudPanel`, `StatusIndicator`, `SubsystemStatusBar`, and real local `DigitalClock`.
- `gui/widgets/ai_core_widget.py`: original faceted synthetic mask, orbital reasoning core, state colors, real microphone ring, and structured-action event nodes.
- `gui/widgets/dashboard_panels.py`: conversation, voice waveform, current task, reasoning summary, Hermes, capabilities, applications, Office/browser, system metrics, task timeline, and quick actions.

## Real State Sources

| Visible area | Authoritative source |
|---|---|
| Voice, wake word, Whisper, speech | `VoiceState.snapshot()` |
| Kimi/OpenRouter, Hermes, memory, news | `AssistantController.status_snapshot()` |
| Browser and Office state | controller snapshot plus `SessionRegistry.get_status()` |
| Current task and Word progress | `LiveTask.snapshot()` |
| Capabilities and permissions | `CapabilityRegistry.report()` |
| Applications and ownership | `SessionRegistry.get_status()` |
| CPU, RAM, disk, network, GPU, threads | `CapabilityHealth.system_metrics()` |
| Timeline and action graph | controller timeline callbacks |
| Confirmation state | `confirmationRequested` and `confirmationResult` |
| Conversation | transcription, typed input, response, and log callbacks |

Unknown values remain `Unavailable`, `Disconnected`, `Waiting`, or `Not configured`. The live preview remains `Unavailable` because no safe event-driven preview is currently supplied by the backend.

## Real Controls

Start/stop voice, mute speech, open browser, open application, open folder, screenshot, self-test, capability page, logs, settings, stop task, emergency stop, task pause/resume/cancel, application focus/close/close-all, news refresh/read/open/save, and research save requests all invoke controller or service APIs. No visible button is decorative.
