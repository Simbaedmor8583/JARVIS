"""
Listener — faster-whisper STT with webrtcvad silence detection.

Records from the default microphone at 16 kHz, starts when speech begins,
stops ~0.8 s after you stop talking, then transcribes locally. GPU is
used automatically when available, else CPU int8.
"""
import threading

import numpy as np

from config import Config

SAMPLE_RATE = 16000
FRAME_MS = 30
FRAME_SAMPLES = int(SAMPLE_RATE * FRAME_MS / 1000)      # 480


class Listener:
    def __init__(self, model_size=None):
        self.model_size = model_size or Config.WHISPER_MODEL
        self._model = None
        self._vad = None
        self._load_lock = threading.Lock()
        self.load_error = ""
        self._ensure_vad()

    def _ensure_vad(self):
        if self._vad is not None:
            return True
        try:
            import webrtcvad
            self._vad = webrtcvad.Vad(2)
            return True
        except Exception as exc:
            self.load_error = f"Voice activity detector unavailable: {exc}"
            return False

    # ---------------------------------------------------------------- load
    def preload(self):
        self._ensure_loaded()

    def _ensure_loaded(self):
        if self._model is not None:
            return True
        if not self._ensure_vad():
            return False
        with self._load_lock:
            if self._model is not None:
                return True
            try:
                from faster_whisper import WhisperModel
                device, compute = "cpu", "int8"
                if Config.WHISPER_DEVICE in ("cpu", "cuda"):
                    device = Config.WHISPER_DEVICE
                    compute = "float16" if device == "cuda" else "int8"
                elif Config.GPU_ENABLED:
                    try:
                        import torch
                        if torch.cuda.is_available():
                            device, compute = "cuda", "float16"
                    except Exception:
                        pass
                self._model = WhisperModel(
                    self.model_size, device=device, compute_type=compute
                )
                return True
            except Exception as exc:
                self.load_error = str(exc)
                self._model = None
                return False

    # ------------------------------------------------------------- record
    def record(self, max_seconds=None, start_timeout=5.0, silence_frames=26):
        """
        Record until end-of-speech. Returns int16 numpy array (may be empty
        if nothing was heard within start_timeout).
        """
        import sounddevice as sd
        if not self._ensure_vad():
            return np.array([], dtype=np.int16)
        max_seconds = max_seconds or Config.LISTEN_MAX_SECONDS
        max_frames = int(max_seconds * 1000 / FRAME_MS)
        start_timeout_frames = int(start_timeout * 1000 / FRAME_MS)

        frames = []
        voiced_run = 0
        started = False
        silent_run = 0
        waited = 0

        with sd.InputStream(
            samplerate=SAMPLE_RATE, channels=1, dtype="int16",
            blocksize=FRAME_SAMPLES,
        ) as stream:
            for _ in range(max_frames):
                data, _ = stream.read(FRAME_SAMPLES)
                pcm = np.frombuffer(data, dtype=np.int16).tobytes()
                try:
                    is_voiced = self._vad.is_speech(pcm, SAMPLE_RATE)
                except Exception:
                    is_voiced = False

                if not started:
                    waited += 1
                    if is_voiced:
                        voiced_run += 1
                    else:
                        voiced_run = max(0, voiced_run - 1)
                    if voiced_run >= 3:               # ~90 ms of voice
                        started = True
                        frames.append(pcm)
                    elif waited > start_timeout_frames:
                        return np.array([], dtype=np.int16)
                else:
                    frames.append(pcm)
                    if is_voiced:
                        silent_run = 0
                    else:
                        silent_run += 1
                        if silent_run >= silence_frames:   # ~0.8 s of silence
                            break

        if not frames:
            return np.array([], dtype=np.int16)
        return np.frombuffer(b"".join(frames), dtype=np.int16)

    # ----------------------------------------------------------- transcribe
    def transcribe(self, audio_i16):
        if audio_i16 is None or len(audio_i16) < SAMPLE_RATE // 4:
            return ""
        audio_f32 = audio_i16.astype(np.float32) / 32768.0
        try:
            segments, _ = self._model.transcribe(
                audio_f32,
                beam_size=1,
                vad_filter=True,
                language="en",
                condition_on_previous_text=False,
            )
            text = " ".join(seg.text for seg in segments).strip()
            # whisper sometimes hallucinates on silence/noise
            if text.lower() in {
                "thank you.", "thanks for watching.", "bye.", "you",
                "subtitle by", "subtitles by",
            }:
                return ""
            return text
        except Exception as exc:
            self.load_error = str(exc)
            return ""

    # ---------------------------------------------------------------- API
    def listen(self, max_seconds=None):
        """Full cycle: record -> transcribe -> text ('' if nothing heard)."""
        if not self._ensure_loaded():
            return ""
        audio = self.record(max_seconds=max_seconds)
        return self.transcribe(audio)

    def listen_quick(self, max_seconds=1.6):
        """Short capture for barge-in monitoring. Returns text or ''."""
        if not self._ensure_loaded():
            return ""
        try:
            audio = self.record(max_seconds=max_seconds, start_timeout=max_seconds,
                                silence_frames=16)
            if len(audio) == 0:
                return ""
            return self.transcribe(audio)
        except Exception:
            return ""
