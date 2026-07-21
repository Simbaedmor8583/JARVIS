"""
DesktopAgent - JARVIS's single, unified control service for the interactive
Windows desktop.

ONE service coordinates application/window/mouse/keyboard/clipboard/screen/
browser/office/file control. The AssistantController and planner call into
this; nothing builds a separate disconnected automation path.

Control preference order (most reliable first):
  1. Native application APIs
  2. Microsoft Office COM automation
  3. Browser DOM automation
  4. Windows UI Automation
  5. Mouse & keyboard automation (final fallback only)

Safety: sensitive actions go through confirm(); every automation can be
cancelled via the shared stop event; pressed keys/buttons are always released
on stop so the agent never leaves anything held down.
"""
import threading
import time

from voice import audio_log
from core.action_manager import Action  # Import the Action dataclass

# automation status surfaced in the GUI
STATUS_WAITING = "Waiting"
STATUS_LOCATING = "Locating target"
STATUS_MOVING = "Moving pointer"
STATUS_CLICKING = "Clicking"
STATUS_TYPING = "Typing"
STATUS_SAVING = "Saving"
STATUS_COMPLETED = "Completed"
STATUS_FAILED = "Failed"
STATUS_CANCELLED = "Cancelled"


class DesktopAgent:
    def __init__(self, controller):
        self.controller = controller
        self.ctx = controller.ctx
        self._stop = threading.Event()
        self._confirm_handler = None
        self._status_cb = None
        self._held_keys = set()
        self._current_task = ""
        self._uia = None

    @property
    def uia(self):
        if self._uia is None:
            from core.ui_automation import WindowsUIAutomation
            self._uia = WindowsUIAutomation()
        return self._uia

    # ---------------------------------------------------------------- wiring
    def set_status_callback(self, fn):
        self._status_cb = fn

    def set_confirm_handler(self, fn):
        """Set the UI decision provider for sensitive actions."""
        self._confirm_handler = fn

    def _status(self, status, detail=""):
        self._current_task = detail
        if self._status_cb is not None:
            try:
                self._status_cb(status, detail)
            except Exception:  # TODO: log this
                pass
        audio_log.log(f"[agent] {status}: {detail}")

    # ---------------------------------------------------------------- safety
    def confirm(self, action: Action):
        """Ask the user before a sensitive action. Default-deny if no handler."""
        if self._confirm_handler is None:
            action_id = getattr(action, "action_id", str(action))
            audio_log.log(f"[agent] confirmation required but no handler: {action_id}")
            return False
        try:
            return self._confirm_handler(action)
        except Exception:
            return False

    def request_stop(self):
        """Emergency stop: cancel current work and release all inputs."""
        self._stop.set()
        self._release_all()
        self._status(STATUS_CANCELLED, "stopped by user")
        audio_log.log("[agent] EMERGENCY STOP - released all keys/buttons")

    def _release_all(self):
        """Release every held key and mouse button immediately."""
        try:
            import pyautogui
            for key in list(self._held_keys):
                try:
                    pyautogui.keyUp(key)
                except Exception:
                    pass
            self._held_keys.clear()
            for btn in ("left", "right", "middle"):
                try:
                    pyautogui.mouseUp(button=btn)
                except Exception:
                    pass
        except Exception:
            pass

    def _check_stop(self):
        if self._stop.is_set():
            self._release_all()
            raise _AgentCancelled()

    def clear_stop(self):
        self._stop.clear()

    # ---------------------------------------------------------------- apps / windows
    def open_application(self, name):
        from skills.system_control import open_thing
        self._status(STATUS_LOCATING, f"open {name}")
        result = open_thing(name, self.ctx, preferred_kind="app")
        self._status(STATUS_COMPLETED, result)
        return result

    def close_application(self, name):
        from skills.system_control import close_thing
        self._status(STATUS_LOCATING, f"close {name}")
        result = close_thing(name, self.ctx)
        self._status(STATUS_COMPLETED, result)
        return result

    def window_action(self, name, action):
        from skills import window_control
        fn = {
            "front": window_control.bring_to_front,
            "focus": window_control.focus_window,
            "minimize": window_control.minimize_window,
            "maximize": window_control.maximize_window,
            "restore": window_control.restore_window,
        }.get(action)
        if fn is None:
            return f"Unknown window action: {action}"
        self._status(STATUS_LOCATING, f"{action} {name}")
        result = fn(name, self.ctx)
        self._status(STATUS_COMPLETED, result)
        return result

    # ---------------------------------------------------------------- mouse
    def move_pointer(self, x, y):
        self._check_stop()
        import pyautogui
        self._status(STATUS_MOVING, f"to {x},{y}")
        pyautogui.moveTo(int(x), int(y))
        self._status(STATUS_COMPLETED, "moved")

    def click(self, x=None, y=None, button="left", clicks=1):
        self._check_stop()
        import pyautogui
        if x is not None and y is not None:
            pyautogui.moveTo(int(x), int(y))
        self._status(STATUS_CLICKING, f"at {x},{y}")
        pyautogui.click(button=button, clicks=clicks)
        self._status(STATUS_COMPLETED, "clicked")

    def double_click(self, x=None, y=None):
        return self.click(x, y, clicks=2)

    def right_click(self, x=None, y=None):
        return self.click(x, y, button="right")

    def scroll(self, amount, direction="down"):
        self._check_stop()
        import pyautogui
        clicks = -abs(int(amount)) if direction == "down" else abs(int(amount))
        pyautogui.scroll(clicks)
        return f"Scrolled {direction}."

    def drag(self, x1, y1, x2, y2):
        self._check_stop()
        import pyautogui
        self._status(STATUS_MOVING, "drag")
        pyautogui.moveTo(int(x1), int(y1))
        pyautogui.dragTo(int(x2), int(y2), duration=0.3, button="left")
        self._status(STATUS_COMPLETED, "dragged")

    # ---------------------------------------------------------------- keyboard
    def type_text(self, text, interval=0.01):
        self._check_stop()
        import pyautogui
        self._status(STATUS_TYPING, f"{len(text)} chars")
        try:
            pyautogui.typewrite(str(text), interval=interval)
            self._status(STATUS_COMPLETED, "typed")
            return "Typed."
        except Exception as exc:
            self._status(STATUS_FAILED, str(exc))
            return f"Type failed: {exc}"

    def press_key(self, key):
        self._check_stop()
        import pyautogui
        self._held_keys.add(key)
        try:
            pyautogui.press(key)
        finally:
            self._held_keys.discard(key)
        return f"Pressed {key}."

    def hotkey(self, *keys):
        self._check_stop()
        import pyautogui
        self._status(STATUS_TYPING, "+".join(keys))
        for key in keys:
            self._held_keys.add(key)
        try:
            pyautogui.hotkey(*keys)
        finally:
            for key in keys:
                self._held_keys.discard(key)
        self._status(STATUS_COMPLETED, "shortcut sent")
        return f"Pressed {'+'.join(keys)}."

    def save_shortcut(self):
        return self.hotkey("ctrl", "s")

    def select_all(self):
        return self.hotkey("ctrl", "a")

    def copy(self):
        return self.hotkey("ctrl", "c")

    def paste(self):
        return self.hotkey("ctrl", "v")

    def undo(self):
        return self.hotkey("ctrl", "z")

    def redo(self,):
        return self.hotkey("ctrl", "y")

    def switch_window(self):
        return self.hotkey("alt", "tab")

    def close_active_window(self):
        return self.hotkey("alt", "F4")

    # ---------------------------------------------------------------- clipboard
    def clipboard_read(self):
        try:
            import pyperclip
            return pyperclip.paste()
        except Exception:
            return ""

    def clipboard_write(self, text):
        try:
            import pyperclip
            pyperclip.copy(str(text))
            return True
        except Exception:
            return False

    # ---------------------------------------------------------------- screen
    def screenshot(self, path=None, active_window=False):
        import pyautogui
        self._status(STATUS_LOCATING, "capturing screen")
        if path is None:
            ts = time.strftime("%Y%m%d_%H%M%S")
            from config import Config
            path = str(Config.DATA_DIR / f"screenshot_{ts}.png")
        try:
            img = pyautogui.screenshot()
            img.save(path)
            self._status(STATUS_COMPLETED, path)
            return path
        except Exception as exc:
            self._status(STATUS_FAILED, str(exc))
            return ""

    def active_window_title(self):
        try:
            import pygetwindow as gw
            win = gw.getActiveWindow()
            return win.title if win is not None else ""
        except Exception:
            return ""

    def verify_target_window(self, title, process_name="", editor_types=()):
        self._check_stop()
        return self.uia.verify_window(
            title=title, process_name=process_name, editor_types=editor_types,
        )

    def click_ui_element(self, window_title, *, title="", auto_id="", control_type=""):
        self._check_stop()
        window = self.uia.focus_window(window_title)
        element = self.uia.find_element(
            window, title=title, auto_id=auto_id, control_type=control_type,
        )
        return self.uia.click_element(element)

    def set_ui_value(self, window_title, value, *, title="", auto_id="", control_type="Edit"):
        self._check_stop()
        window = self.uia.focus_window(window_title)
        element = self.uia.find_element(
            window, title=title, auto_id=auto_id, control_type=control_type,
        )
        return self.uia.set_value(element, value)

    # ---------------------------------------------------------------- reading
    def read_aloud(self, text):
        self.controller.speak(text)

    # ---------------------------------------------------------------- tasks
    def run_task(self, description, steps):
        """Run a list of (name, callable) steps with stop + status reporting."""
        self.clear_stop()
        results = []
        for name, fn in steps:
            try:
                self._check_stop()
            except _AgentCancelled:
                results.append((name, "cancelled"))
                break
            self._status(STATUS_WAITING, name)
            try:
                results.append((name, fn()))
            except _AgentCancelled:
                results.append((name, "cancelled"))
                break
            except Exception as exc:
                audio_log.log_error(f"[agent] step '{name}' failed: {exc}", exc)
                results.append((name, f"failed: {exc}"))
        self._status(STATUS_COMPLETED, description)
        return results


class _AgentCancelled(Exception):
    pass
