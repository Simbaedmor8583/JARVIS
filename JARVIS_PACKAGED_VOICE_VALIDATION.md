# JARVIS Packaged Voice Validation

Date: 2026-07-20

## Target

- Executable: `release\JARVIS-GUI\JARVIS.exe`
- SHA-256: `7210C318BF0EDA12ECEEEBDB0896C0C63E3C5FF733ADF1ACC439F20C95192235`

## Automated Packaged Voice Startup

- Start Voice invoked through the packaged GUI.
- A real input device was enumerated and opened: USB PnP microphone.
- Wake-word worker started.
- `hey_jarvis` model loaded at threshold 0.5.
- Voice engine thread started.
- GUI entered listening/recording state from live microphone state.
- No `WakeWordEngine.process()` missing-method or wake processing error appeared.
- Stop Voice closed the microphone stream and worker cleanly.
- Final application exit stopped voice workers again and completed controller shutdown.

Result: **PASS** for packaged microphone, wake-word startup, GUI voice state, and clean stop.

## Loop And Command Repair

- Fixed the five-second wake wait timeout being treated as a real wake event.
- Suppressed wake inference while Piper is speaking and during an active command session.
- Initialized WebRTC VAD independently of Whisper preload so `--skip-model-preload` can still record commands.
- Restored the active USB microphone gain and selected it explicitly in the persisted JARVIS settings.
- Packaged acoustic wake score reached `0.97` at the configured `0.50` threshold.
- The packaged app recorded speech, produced a 24-character transcription, sent it through the real router, and returned a response.
- A subsequent 75-second normal-mode soak produced zero false wakes, zero false transcriptions, and no repeated Piper prompts.

Result: **PASS** for packaged acoustic wake, recording, transcription, routing, response, and loop suppression.

## Confirmation Speech Coverage

Automated tests passed for voice `yes`, `no`, and `cancel` while a confirmation was pending. These tests validate controller routing and safe execution behavior but are not a substitute for a human-spoken packaged command.

## Human-Spoken Validation

No real human-spoken command was performed in this automated session. The end-to-end result above used an operating-system speech synthesizer played through the real speakers and captured by the real microphone.

Human voice result: **NOT EXECUTED**.

Release status: **NOT READY** until at least one required command is spoken by a human through the packaged executable and its transcript-to-action result is recorded.
