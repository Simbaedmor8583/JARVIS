from types import SimpleNamespace

from core.ui_automation import WindowsUIAutomation


class FakeWindow:
    def __init__(self):
        self.element_info = SimpleNamespace(name="Document - Microsoft Word")
        self.focused = False

    def exists(self, timeout=0):
        return True

    def restore(self):
        return None

    def set_focus(self):
        self.focused = True

    def process_id(self):
        return 42

    def descendants(self):
        return [SimpleNamespace(element_info=SimpleNamespace(control_type="Document"))]


class FakeDesktop:
    def __init__(self, window):
        self._window = window
        self.kwargs = None

    def window(self, **kwargs):
        self.kwargs = kwargs
        return self._window


def test_uia_focuses_verified_window(monkeypatch):
    window = FakeWindow()
    desktop = FakeDesktop(window)
    automation = WindowsUIAutomation()
    monkeypatch.setattr(automation, "desktop", lambda: desktop)
    assert automation.focus_window("Microsoft Word") is window
    assert window.focused is True
    assert "Microsoft\\ Word" in desktop.kwargs["title_re"]


def test_uia_verifies_editor_control(monkeypatch):
    window = FakeWindow()
    automation = WindowsUIAutomation()
    monkeypatch.setattr(automation, "find_window", lambda title="", process=None: window)
    assert automation.verify_window(title="Microsoft Word", editor_types=("Document",)) is True
    assert automation.verify_window(title="Excel", editor_types=("Document",)) is False
