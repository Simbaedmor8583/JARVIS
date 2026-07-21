"""Reusable voice pipeline facade for wake, transcription, speech, and barge-in."""
import threading
import time

from voice.listener import Listener
from voice.speaker import Speaker
from voice.wakeword import WakeWordEngine


class VoicePipeline:
    def __init__(self, listener=None, speaker=None, wakeword=None):
        self.listener = listener or Listener()
        self.speaker = speaker or Speaker()
        self.wakeword = wakeword or WakeWordEngine()
        self.stop_event = threading.Event()
        self._barge_thread = None

    def start_barge_monitor(self):
        if self._barge_thread and self._barge_thread.is_alive():
            return
        self._barge_thread = threading.Thread(target=self._monitor, daemon=True)
        self._barge_thread.start()

    def _monitor(self):
        while not self.stop_event.is_set():
            if not self.speaker.speaking:
                time.sleep(0.2)
                continue
            heard = self.listener.listen_quick(max_seconds=1.6)
            if heard and "stop" in heard.lower():
                self.speaker.stop()

    def wait_for_command(self):
        if not self.wakeword.wait(stop_event=self.stop_event):
            return ""
        if self.speaker.speaking:
            self.speaker.stop()
        return self.listener.listen()

    def close(self):
        self.stop_event.set()
        self.speaker.stop()
