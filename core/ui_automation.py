"""Windows UI Automation primitives used before keyboard/mouse fallbacks."""
from __future__ import annotations

import re


class WindowsUIAutomation:
    def __init__(self, backend="uia"):
        self.backend = backend

    def desktop(self):
        from pywinauto import Desktop
        return Desktop(backend=self.backend)

    def find_window(self, title="", process=None):
        desktop = self.desktop()
        kwargs = {}
        if title:
            kwargs["title_re"] = f".*{re.escape(str(title))}.*"
        if process is not None:
            kwargs["process"] = int(process)
        window = desktop.window(**kwargs)
        if not window.exists(timeout=5):
            raise RuntimeError(f"Window not found: {title or process}")
        return window

    def focus_window(self, title="", process=None):
        window = self.find_window(title, process)
        try:
            window.restore()
        except Exception:
            pass
        window.set_focus()
        return window

    def verify_window(self, *, title="", process_name="", editor_types=()):
        window = self.find_window(title)
        element = window.element_info
        actual_title = str(getattr(element, "name", "") or "")
        if title and title.lower() not in actual_title.lower():
            return False
        if process_name:
            try:
                import psutil
                actual_process = psutil.Process(window.process_id()).name()
                if actual_process.lower() != process_name.lower():
                    return False
            except Exception:
                return False
        if editor_types:
            descendants = window.descendants()
            if not any(str(getattr(item.element_info, "control_type", "")) in editor_types for item in descendants):
                return False
        return True

    def find_element(self, window, *, title="", auto_id="", control_type=""):
        kwargs = {}
        if title:
            kwargs["title_re"] = f".*{re.escape(str(title))}.*"
        if auto_id:
            kwargs["auto_id"] = str(auto_id)
        if control_type:
            kwargs["control_type"] = str(control_type)
        element = window.child_window(**kwargs)
        if not element.exists(timeout=5):
            raise RuntimeError("UI Automation element not found")
        return element

    def click_element(self, element):
        element.wait("visible enabled ready", timeout=10)
        element.click_input()
        return True

    def set_value(self, element, value):
        element.wait("visible enabled ready", timeout=10)
        try:
            element.set_edit_text(str(value))
        except Exception:
            element.set_focus()
            element.type_keys(str(value), with_spaces=True, set_foreground=False)
        return True

    def detect_dialogs(self, title=""):
        window = self.find_window(title)
        return [
            child for child in window.children()
            if str(getattr(child.element_info, "control_type", "")) == "Window"
        ]
