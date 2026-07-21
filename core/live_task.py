"""Shared execution controls for visible, cancellable desktop tasks."""
import threading
from dataclasses import dataclass, field


FAST_BACKGROUND = "FAST_BACKGROUND"
LIVE_INTERACTIVE = "LIVE_INTERACTIVE"
PHYSICAL_INPUT = "PHYSICAL_INPUT"


@dataclass
class LiveTaskState:
    task_id: str = ""
    description: str = ""
    application: str = ""
    step: str = ""
    mode: str = FAST_BACKGROUND
    progress: int = 0
    status: str = "idle"
    delay_ms: int = 20
    metadata: dict = field(default_factory=dict)


class LiveTaskController:
    """Thread-safe pause, resume, speed, and cancellation state."""

    def __init__(self, on_change=None):
        self._lock = threading.RLock()
        self._resume = threading.Event()
        self._resume.set()
        self._cancel = threading.Event()
        self._on_change = on_change
        self.state = LiveTaskState()

    def start(self, task_id, description, application="", mode=FAST_BACKGROUND):
        with self._lock:
            self._cancel.clear()
            self._resume.set()
            self.state = LiveTaskState(
                task_id=str(task_id), description=str(description),
                application=str(application), mode=str(mode), status="running",
            )
        self._notify()

    def update(self, step=None, progress=None, **metadata):
        with self._lock:
            if step is not None:
                self.state.step = str(step)
            if progress is not None:
                self.state.progress = max(0, min(100, int(progress)))
            if metadata:
                self.state.metadata.update(metadata)
        self._notify()

    def pause(self):
        with self._lock:
            if self.state.status == "running":
                self.state.status = "paused"
                self._resume.clear()
        self._notify()
        return "Task paused, sir."

    def resume(self):
        with self._lock:
            if self.state.status == "paused":
                self.state.status = "running"
            self._resume.set()
        self._notify()
        return "Task resumed, sir."

    def cancel(self):
        with self._lock:
            self.state.status = "cancelled"
            self._cancel.set()
            self._resume.set()
        self._notify()
        return "Task cancelled, sir."

    def set_speed(self, direction):
        with self._lock:
            if direction == "faster":
                self.state.delay_ms = max(0, self.state.delay_ms - 5)
            else:
                self.state.delay_ms = min(250, self.state.delay_ms + 5)
            delay = self.state.delay_ms
        self._notify()
        return f"Typing delay set to {delay} milliseconds, sir."

    def checkpoint(self):
        self._resume.wait()
        if self._cancel.is_set():
            raise TaskCancelled()

    def complete(self):
        with self._lock:
            self.state.status = "completed"
            self.state.progress = 100
        self._notify()

    def fail(self, detail=""):
        with self._lock:
            self.state.status = "failed"
            if detail:
                self.state.metadata["error"] = str(detail)
        self._notify()

    def snapshot(self):
        with self._lock:
            return {
                "task_id": self.state.task_id,
                "description": self.state.description,
                "application": self.state.application,
                "step": self.state.step,
                "mode": self.state.mode,
                "progress": self.state.progress,
                "status": self.state.status,
                "delay_ms": self.state.delay_ms,
                "metadata": dict(self.state.metadata),
            }

    def _notify(self):
        if self._on_change is not None:
            try:
                self._on_change(self.snapshot())
            except Exception:
                pass


class TaskCancelled(Exception):
    pass
