"""Unified Windows application, file, folder, URI, and window control."""
import os
from pathlib import Path
from urllib.parse import urlparse

from core.application_registry import ApplicationRegistry


class WindowsController:
    def __init__(self, ctx):
        self.ctx = ctx
        self.applications = ApplicationRegistry()

    def open_application(self, name):
        from skills.system_control import open_thing
        return open_thing(name, self.ctx, preferred_kind="app")

    def open_folder(self, folder):
        from skills.system_control import open_thing
        return open_thing(folder, self.ctx, preferred_kind="folder")

    def open_file(self, file_path):
        from skills.system_control import open_thing
        return open_thing(file_path, self.ctx, preferred_kind="file")

    def open_uri(self, uri):
        parsed = urlparse(str(uri))
        if parsed.scheme in ("http", "https"):
            page = self.ctx.browser.open_site(str(uri))
            return f"Opening {uri}." if page is not None else f"I couldn't open {uri}."
        if parsed.scheme not in ("ms-settings", "mailto"):
            return "That URI scheme is not approved."
        os.startfile(str(uri))
        self.ctx.registry.register("app", str(uri), extra={"uri": str(uri)})
        return f"Opening {uri}."

    def find_windows(self, title=""):
        try:
            import pygetwindow as gw
            windows = gw.getAllWindows()
            if title:
                title_low = title.lower()
                windows = [window for window in windows
                           if window.title and title_low in window.title.lower()]
            return windows
        except Exception:
            return []

    def focus_window(self, title):
        return self._window_action(title, "activate")

    def minimize_window(self, title):
        return self._window_action(title, "minimize")

    def maximize_window(self, title):
        return self._window_action(title, "maximize")

    def restore_window(self, title):
        return self._window_action(title, "restore")

    def move_window(self, title, x, y):
        windows = self.find_windows(title)
        if not windows:
            return False
        windows[0].moveTo(int(x), int(y))
        return True

    def resize_window(self, title, width, height):
        windows = self.find_windows(title)
        if not windows:
            return False
        windows[0].resizeTo(int(width), int(height))
        return True

    def close_window(self, title):
        windows = self.find_windows(title)
        if not windows:
            return False
        windows[0].close()
        return True

    def close_application(self, name):
        from skills.system_control import close_thing
        return close_thing(name, self.ctx)

    def close_recent_jarvis_item(self):
        from skills.system_control import close_thing
        return close_thing("", self.ctx)

    def close_all_jarvis_items(self):
        from skills.system_control import close_thing
        return close_thing("__all__", self.ctx)

    def close_resource(self, reference):
        from skills.system_control import close_thing
        return close_thing(reference, self.ctx)

    def _window_action(self, title, action):
        windows = self.find_windows(title)
        if not windows:
            return False
        getattr(windows[0], action)()
        return True
