"""
Shared speech-output service.

Wraps the existing Speaker (Edge TTS -> Piper fallback -> pygame playback)
and reports a real status to the GUI: unavailable / ready / speaking /
muted / error. "Speaker OFF" is only ever shown when speech truly is
unavailable - never merely because Edge TTS failed while Piper is fine.
"""
import threading

from voice import audio_log
from config import Config


class SpeechOutputService:
    def __init__(self, speaker=None, state=None):
        self.speaker = speaker
        self.state = state
        self._muted = False
        self._lock = threading.RLock()
        self._speaker_state = "ready"
        self._engine = "Piper Offline"
        self._available = True

    def attach(self, speaker, state):
        self.speaker = speaker
        self.state = state

    def _set(self, **kwargs):
        if self.state is not None:
            self.state.update(**kwargs)

    @property
    def muted(self):
        return self._muted

    @property
    def speaking(self):
        return bool(self.speaker is not None and self.speaker.speaking)

    def available(self):
        return self._available

    def speak(self, text, block=False):
        if self._muted:
            audio_log.log("Speak suppressed (muted)")
            self._set(speaker_state="muted")
            return
        if self.speaker is None:
            self._set(speaker_state="unavailable", speaker_available=False)
            return
        self._set(speaker_state="speaking", speaker_available=True,
                  speaker_engine=self._engine)
        audio_log.log("Piper playback started")
        try:
            self.speaker.speak(text, block=block)
        except Exception as exc:
            audio_log.log_error(f"Speech error: {exc}", exc)
            self._set(speaker_state="error")
            return
        # return to ready shortly after queueing (Speaker is async)
        engine = getattr(self.speaker, "last_engine", "") or self._engine
        pretty = "Piper Offline" if "piper" in engine.lower() else "Edge TTS"
        self._set(speaker_engine=pretty)
        self._set(speaker_state="speaking" if self.speaker.speaking else "ready")
        audio_log.log("Piper playback completed" if not self.speaker.speaking
                      else "Piper playback queued")

    def note_engine(self):
        if self.speaker is None:
            return
        engine = getattr(self.speaker, "last_engine", "") or "piper"
        pretty = "Piper Offline" if "piper" in engine.lower() else "Edge TTS"
        if not Config.EDGE_TTS_ENABLED:
            pretty = "Piper Offline"
        self._set(speaker_engine=pretty, speaker_available=True,
                  speaker_state="ready" if not self._muted else "muted")

    def sync_state(self):
        if self.speaker is None:
            self._set(speaker_available=False, speaker_state="unavailable")
            return
        if self._muted:
            self._set(speaker_state="muted", speaker_available=True)
        elif self.speaker.speaking:
            self._set(speaker_state="speaking", speaker_available=True)
        else:
            self._set(speaker_state="ready", speaker_available=True)

    def mute(self):
        with self._lock:
            self._muted = True
        try:
            if self.speaker is not None:
                self.speaker.stop()
        except Exception:
            pass
        self._set(speaker_state="muted")
        audio_log.log("Speaker muted")

    def unmute(self):
        with self._lock:
            self._muted = False
        self._set(speaker_state="ready")
        audio_log.log("Speaker unmuted")

    def stop(self):
        try:
            if self.speaker is not None:
                self.speaker.stop()
        except Exception:
            pass

    def wait(self, timeout=None):
        if self.speaker is not None:
            self.speaker.wait(timeout=timeout)
