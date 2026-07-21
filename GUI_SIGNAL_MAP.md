# JARVIS GUI Signal Map

Date: 2026-07-20

All controller callbacks enter `gui/workers.py::ControllerBridge`. Qt delivers GUI updates on the GUI thread. Typed commands use the persistent `JARVIS-GUI-Commands` worker so Playwright actions retain thread affinity.

| Semantic signal | Derived from | GUI consumer |
|---|---|---|
| `state_changed` | controller state callback | state banner and AI core |
| `voice_state_changed` | `VoiceState.snapshot()` | voice panel and subsystem rail |
| `microphone_level_changed` | `input_level` | waveforms and AI core |
| `wake_word_state_changed` | wake-word callback | subsystem rail |
| `transcript_changed` | transcription callback | conversation voice text |
| `cleaned_command_changed` | `cleaned` timeline event | conversation and goal summary |
| `planner_state_changed` | processing/planner events | safe execution summary |
| `hermes_state_changed` | status snapshot | Hermes panel; currently disabled |
| `task_started`, `task_progress` | live-task snapshot | task panels and progress |
| `task_step_started/completed/failed` | timeline events | timeline and action nodes |
| `task_waiting_confirmation` | confirmation timeline/request | amber AI core state |
| `task_completed/cancelled/failed` | task/timeline state | task pages and AI core |
| `speech_started/level/finished` | speaker state | speaking state and waveform |
| `capability_status_changed` | capability report | dashboard and capability page |
| `application_opened/closed` | registry snapshot delta | applications/automation pages |
| `application_focused` | reserved for a future authoritative focus callback | not synthesized |
| `browser_state_changed` | status snapshot | workspace panel |
| `office_state_changed` | status snapshot | workspace panel |
| `research_state_changed` | status/task snapshots | research page |
| `system_metrics_changed` | real health metrics | circular gauges and detail line |
| `audit_event` | timeline/log callbacks | logs and timeline pages |
| `emergency_stop_triggered` | emergency-stop control | cancellation state |

Existing compatibility signals (`stateChanged`, `statusChanged`, `transcription`, `response`, `timeline`, `registry`, `logLine`, `wakeword`, `voicestate`, `agentstatus`, `capabilities`, and `taskstatus`) remain intact.
