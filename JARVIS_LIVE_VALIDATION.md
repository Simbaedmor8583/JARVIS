# JARVIS Live Validation

Date: 2026-07-20

## Files Changed

- Backend/security: `config.py`, `main.py`, `brain/llm.py`, `brain/router.py`, `core/action_manager.py`, `core/application_registry.py`, `core/assistant_controller.py`, `core/capability_health.py`, `core/capability_registry.py`, `core/desktop_agent.py`, `core/live_task.py`, `core/planner.py`, `core/registry.py`, `core/save_workflow.py`, `core/windows_controller.py`.
- Skills/voice: `skills/browser.py`, `skills/coder.py`, `skills/office.py`, `skills/office_service.py`, `skills/research.py`, `skills/system_control.py`, `skills/windows_targets.py`, `skills/word_skill.py`, `voice/engine.py`.
- GUI/startup: `desktop_main.py`, `gui/capabilities_page.py`, `gui/core_widget.py`, `gui/main_window.py`, `gui/workers.py`, `pytest.ini`.
- Tests: `tests/test_action_manager.py`, `tests/test_backend_regression.py`, `tests/test_capability_health.py`, `tests/test_capability_registry.py`, `tests/test_confirmation_flow.py`, `tests/test_controller.py`, `tests/test_integration.py`, `tests/test_live_task.py`, `tests/test_registry.py`, `tests/test_registry_window.py`, `tests/test_save_workflow.py`, `tests/test_voice.py`, `tests/test_windows_routing.py`.
- Reports: `JARVIS_ROUTING_TRACE.md`, `JARVIS_WINDOWS_CONTROL_REPORT.md`, `JARVIS_LIVE_WORD_REPORT.md`, `JARVIS_SAVE_WORKFLOW_REPORT.md`, `JARVIS_LIVE_VALIDATION.md`, `JARVIS_CAPABILITY_REGISTRY_REPORT.md`, `GUI_ARCHITECTURE.md`, `GUI_SIGNAL_MAP.md`, `GUI_THEME_GUIDE.md`, `GUI_PERFORMANCE_REPORT.md`.
- Backup: `.backups/assistant_controller.py.before_capability_registry`.

## Automated

- Python compilation: passed for all source and test modules.
- Collected: 201.
- Passed: 201.
- Failed: 0.
- Skipped: 0.

## Desktop Results

| Validation | Result |
|---|---|
| Source GUI visible | pass |
| Downloads opens real folder | pass |
| Downloads does not open Word | pass |
| Close folder | pass |
| Open Word | pass |
| Create Word document | pass |
| Live source-grounded Word report | pass |
| Pause | pass |
| Resume | pass |
| Cancel | pass |
| Save-location dialogue | pass |
| Save verification | pass |
| Close Word | pass |
| Open YouTube | pass |
| Close browser | pass |
| GUI confirmation visible | pass |
| Approve once | pass |
| Close all owned resources | pass |
| Preserve pre-existing visible windows | pass |
| Voice engine start/stop | pass |

## Confirmation

The live close-all dialog displayed action name, target, reason, HIGH risk, and exact effect. Approve once closed five owned entries. Deterministic Qt tests additionally cover deny, cancel task, timeout, voice yes, voice no, voice cancel, dialog close, paused execution, denied-action non-execution, redaction, and audit outcomes.

## Voice

The real USB microphone opened, wake word loaded, microphone activity was live, and shutdown succeeded without an audio error. A human-spoken transcript was not recorded during this run; yes/no/cancel routing was validated by driving the real `VoiceEngine` transcription branch in tests.

## Build Gate

Hermes was not installed. The packaged executable was not rebuilt because this phase explicitly prohibited rebuilding.
