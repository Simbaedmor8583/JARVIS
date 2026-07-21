import threading
import time

import pytest

from core.live_task import LIVE_INTERACTIVE, LiveTaskController, TaskCancelled
from skills import word_skill


def test_live_task_pause_resume_and_progress():
    task = LiveTaskController()
    task.start("1", "Write report", "Microsoft Word", LIVE_INTERACTIVE)
    task.update(step="Introduction", progress=25)
    assert task.pause() == "Task paused, sir."
    assert task.snapshot()["status"] == "paused"
    assert task.resume() == "Task resumed, sir."
    assert task.snapshot()["status"] == "running"
    assert task.snapshot()["progress"] == 25


def test_live_task_cancel_interrupts_checkpoint():
    task = LiveTaskController()
    task.start("1", "Write report", mode=LIVE_INTERACTIVE)
    task.cancel()
    with pytest.raises(TaskCancelled):
        task.checkpoint()


def test_live_task_checkpoint_waits_while_paused():
    task = LiveTaskController()
    task.start("1", "Write report", mode=LIVE_INTERACTIVE)
    task.pause()
    passed = threading.Event()

    def worker():
        task.checkpoint()
        passed.set()

    thread = threading.Thread(target=worker)
    thread.start()
    time.sleep(0.05)
    assert not passed.is_set()
    task.resume()
    thread.join(timeout=1)
    assert passed.is_set()


def test_word_com_progressive_insertion(monkeypatch):
    inserted = []

    class FakeWordService:
        process_id = None
        window_handle = None
        def open(self, visible=True):
            assert visible is True
        def new_document(self):
            return object()
        def insert_heading(self, text, level=1, doc=None):
            inserted.append(("heading", text))
        def insert_bullets(self, items, doc=None):
            inserted.append(("bullets", tuple(items)))
        def type_visibly(self, text, doc=None):
            inserted.append(("paragraph", text))
        def save(self, path, doc=None):
            from pathlib import Path
            Path(path).write_bytes(b"docx")

    class FakeLLM:
        available = True
        def quick(self, *args, **kwargs):
            return "# Renewable Energy\n\n## Introduction\n\nClean energy matters."

    class FakeRegistry:
        def register(self, *args, **kwargs):
            return {"id": "document"}
        def update_entry(self, *args, **kwargs):
            return None

    monkeypatch.setattr("skills.office_service.WordService", FakeWordService)
    monkeypatch.setattr(
        "skills.research.build_research_session",
        lambda *args, **kwargs: {
            "abstract": "",
            "draft": {"Introduction": "Clean energy matters."},
            "sources": [],
        },
    )
    task = LiveTaskController()
    task.state.delay_ms = 0
    ctx = type("Ctx", (), {
        "llm": FakeLLM(), "live_task": task, "pending": None, "state": {},
        "registry": FakeRegistry(),
    })()
    result = word_skill.create_live_document("renewable energy", ctx)
    assert result == "The document is ready. Where would you like me to save it?"
    assert inserted == [
        ("heading", "Renewable Energy"),
        ("heading", "Introduction"),
        ("paragraph", "Clean energy matters."),
        ("heading", "References"),
    ]
    assert ctx.pending["kind"] == "save_document"
