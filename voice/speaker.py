"""
Speaker â€” fast TTS with barge-in.

edge-tts synthesizes natural neural voices to MP3 (streamed to disk),
pygame plays it back on a background thread. speak() returns immediately
so JARVIS can talk WHILE working. stop() silences playback instantly â€”
that's what powers "Jarvis stop".
"""
import asyncio
import re
import tempfile
import threading
import time
import wave
from pathlib import Path

from config import Config


def _clean_for_speech(text):
    """Strip markdown-ish artifacts so they aren't read aloud."""
    t = str(text)
    t = re.sub(r"[*_`#>]", "", t)
    t = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", t)   # [label](url) -> label
    t = re.sub(r"https?://\S+", "", t)          # raw URLs
    t = re.sub(r"\s+", " ", t).strip()
    return t


class Speaker:
    def __init__(self, voice=None, rate=None, pitch=None):
        self.voice = voice or Config.TTS_VOICE
        self.rate = rate or f"{round((Config.VOICE_SPEED - 1.0) * 100):+d}%"
        self.pitch = pitch or f"{Config.VOICE_PITCH:+d}Hz"
        self._stop = threading.Event()
        self._speaking = threading.Event()
        self._lock = threading.Lock()
        self._mixer_lock = threading.RLock()
        self._thread_local = threading.local()
        self._thread = None
        self._ready = False
        self._piper_voice = None
        self._piper_lock = threading.Lock()
        self.last_engine = ""
        self._init_mixer()

    # ------------------------------------------------------------ plumbing
    def _init_mixer(self):
        with self._mixer_lock:
            try:
                import pygame
                pygame.mixer.init()
                self._pygame = pygame
                self._ready = True
            except Exception:
                self._pygame = None
                self._ready = False

    @property
    def speaking(self):
        return self._speaking.is_set()

    # ---------------------------------------------------------------- API
    def speak(self, text, block=False):
        """Queue speech. Non-blocking by default; block=True waits for finish."""
        text = _clean_for_speech(text)
        if not text:
            return
        self.stop()
        stop_event = threading.Event()
        t = threading.Thread(
            target=self._run,
            args=(text, stop_event),
            daemon=True,
        )
        with self._lock:
            self._stop = stop_event
            self._thread = t
        t.start()
        if block:
            t.join()

    def stop(self):
        """Barge-in: silence playback immediately."""
        self._stop.set()
        if self._ready:
            with self._mixer_lock:
                try:
                    self._pygame.mixer.music.stop()
                except Exception:
                    pass

    def wait(self, timeout=None):
        """Block until current speech finishes (or timeout seconds)."""
        start = time.time()
        while self._speaking.is_set():
            if timeout and (time.time() - start) > timeout:
                break
            time.sleep(0.05)

    # ------------------------------------------------------------- worker
    def _should_stop(self):
        thread_local = getattr(self, "_thread_local", None)
        local_event = getattr(thread_local, "stop_event", None)
        return (local_event or self._stop).is_set()

    def _run(self, text, stop_event=None):
        if stop_event is not None:
            self._thread_local.stop_event = stop_event
        self._speaking.set()
        tmp_path = None
        try:
            print(f"[JARVIS] {text}", flush=True)
            tmp_path = self._synthesize(text)
            if self._should_stop() or not tmp_path.exists() or tmp_path.stat().st_size == 0:
                return
            with self._mixer_lock:
                if not self._ready:
                    self._init_mixer()
                if not self._ready:
                    return
                self._pygame.mixer.music.load(str(tmp_path))
                self._pygame.mixer.music.play()
                while self._pygame.mixer.music.get_busy():
                    if self._should_stop():
                        break
                    time.sleep(0.03)
                try:
                    self._pygame.mixer.music.stop()
                    self._pygame.mixer.music.unload()
                except Exception:
                    pass
        except Exception as exc:
            print(f"[speaker error] {exc}", flush=True)
        finally:
            if tmp_path is not None:
                try:
                    tmp_path.unlink(missing_ok=True)
                except Exception:
                    pass
            with self._lock:
                if self._thread is threading.current_thread():
                    self._speaking.clear()

    def _temp_path(self, suffix):
        import os
        fd, tmp = tempfile.mkstemp(suffix=suffix, prefix="jarvis_tts_")
        os.close(fd)
        return Path(tmp)

    def _synthesize(self, text):
        # Use Piper immediately when Edge TTS is disabled
        if not Config.EDGE_TTS_ENABLED:
            piper_path = self._temp_path(".wav")
            try:
                self._synth_piper(text, piper_path)
                if piper_path.stat().st_size <= 44:
                    raise RuntimeError("Piper returned no audio")
                self.last_engine = "piper"
                return piper_path
            except Exception:
                piper_path.unlink(missing_ok=True)
                raise

        edge_path = self._temp_path(".mp3")
        try:
            asyncio.run(self._synth_edge(text, edge_path))
            if edge_path.stat().st_size == 0:
                raise RuntimeError("Edge TTS returned no audio")
            self.last_engine = "edge"
            return edge_path
        except Exception as edge_error:
            edge_path.unlink(missing_ok=True)
            print(f"[tts] Edge TTS unavailable ({edge_error}); using offline Piper.", flush=True)

        piper_path = self._temp_path(".wav")
        try:
            self._synth_piper(text, piper_path)
            if piper_path.stat().st_size <= 44:
                raise RuntimeError("Piper returned no audio")
            self.last_engine = "piper"
            return piper_path
        except Exception:
            piper_path.unlink(missing_ok=True)
            raise

    async def _synth_edge(self, text, path: Path):
        import edge_tts
        communicate = edge_tts.Communicate(
            text, self.voice, rate=self.rate, pitch=self.pitch
        )
        with open(path, "wb") as f:
            async for chunk in communicate.stream():
                if self._should_stop():
                    break
                if chunk.get("type") == "audio":
                    f.write(chunk["data"])

    def _synth_piper(self, text, path: Path):
        model_path = Path(Config.PIPER_MODEL)
        if not model_path.exists():
            raise FileNotFoundError(f"Piper model not found: {model_path}")
        with self._piper_lock:
            if self._piper_voice is None:
                from piper import PiperVoice
                self._piper_voice = PiperVoice.load(model_path)
            with wave.open(str(path), "wb") as wav_file:
                self._piper_voice.synthesize_wav(text, wav_file)
