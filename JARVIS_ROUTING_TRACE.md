# JARVIS Routing Trace

Date: 2026-07-20

## Root Cause

The broken runtime had two compounding routing defects:

1. `core/assistant_controller.py::handle_text` had been replaced with a temporary `mock_skill.mock_operation` action instead of calling `main.handle_utterance`. The recovered pre-repair code is preserved at `.backups/assistant_controller.py.before_capability_registry`.
2. Known-folder phrases did not all have deterministic rules ahead of generic application/model routing. Folder wording could therefore reach the local classifier and be interpreted as an Office request.

The controller now performs only command cleanup and registry-command interception, then returns every ordinary command to `main.handle_utterance`. Known folders are matched before generic applications, Office creation, structured planning, and model fallback.

## Current Flow

1. Voice: `VoiceEngine._do_transcription_and_route` -> `AssistantController.handle_text`.
2. Typed: `GuiController.submit_text` -> worker -> `AssistantController.handle_text`.
3. Cleanup: `core.command_text.cleanup_command`.
4. Registry CLI interception: `AssistantController._registry_command`.
5. Real backend: `main.handle_utterance`.
6. Pending dialogue / emergency command handling.
7. Compound planner: `core.planner.plan_command`.
8. Deterministic routing: `brain.router.fast_lane`.
9. Local classifier only when deterministic routing returns no intent.
10. Policy gate: `ActionManager.execute_intent` validates the action and allowlist.
11. Existing dispatch: `main._dispatch_registered` -> real skill module.

## Phrase Traces

| Input | Planner | Deterministic intent | Final execution path |
|---|---|---|---|
| `Open Downloads.` | none | `app.open_folder(target=Downloads)` | `system_control.handle` -> `WindowsController.open_folder` -> `open_thing(preferred_kind=folder)` -> `resolve_windows_target` -> `_launch_resolved` |
| `Open my Downloads folder.` | none | `app.open_folder(target=Downloads)` | same known-folder path |
| `Show my Downloads.` | none | `app.open_folder(target=Downloads)` | same known-folder path |
| `Go to Downloads.` | none | `app.open_folder(target=Downloads)` | same known-folder path |
| `Open Word.` | none | `app.open(target=Word)` | `system_control.handle` -> `open_thing` -> `resolve_windows_target` -> `_launch_resolved` |
| `Open Microsoft Word.` | none | `app.open(target=Word)` | same application path |
| `Create a Word document.` | none | `office_word.create_document` | `word_skill.handle` -> `create_document` -> `WordService.open` -> `WordService.new_document` |

## Validation

- Downloads opened `%USERPROFILE%\Downloads` in Explorer.
- The owned Explorer HWND was live after opening and gone after `Close the folder`.
- WINWORD process state was unchanged throughout the Downloads test.
- Unknown intents are rejected by the allowlist rather than executed.
- No production path contains `mock_skill`, `mock_operation`, or `mock_dangerous_operation`.

