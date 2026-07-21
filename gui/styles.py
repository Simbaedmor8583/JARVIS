"""Original cinematic JARVIS palette and frozen-safe stylesheet loading."""
from pathlib import Path

from config import RESOURCE_DIR

BG_DEEP = "#02070b"
BG_PANEL = "rgba(4, 17, 24, 232)"
BG_PANEL_SOLID = "#061119"
CYAN = "#00d9f5"
CYAN_DIM = "#087e95"
CYAN_GLOW = "#8af6ff"
BLUE_WHITE = "#d8f8ff"
AMBER = "#ffad32"
TEXT = "#d8edf3"
TEXT_DIM = "#6e96a2"
BORDER = "rgba(0, 217, 245, 100)"
DANGER = "#ff574f"
SUCCESS = "#31e6a1"


FALLBACK_QSS = f"""
* {{ font-family: 'Segoe UI', sans-serif; color: {TEXT}; outline: none; }}
QMainWindow, QDialog {{ background: {BG_DEEP}; }}
QFrame#hudPanel {{ background: {BG_PANEL}; border: 1px solid {BORDER}; border-radius: 4px; }}
QLabel#panelTitle {{ color: {CYAN}; font: 700 10px 'Consolas'; letter-spacing: 1px; }}
QLabel#panelMarker {{ color: {CYAN_GLOW}; }}
QLabel#dataValue {{ color: {BLUE_WHITE}; font-size: 10px; }}
QPushButton {{ background: rgba(0,217,245,18); border: 1px solid {BORDER}; padding: 6px; }}
QPushButton:hover {{ background: rgba(0,217,245,45); }}
QPushButton#danger {{ color: #ffd4d1; border-color: rgba(255,87,79,150); }}
QLineEdit, QListWidget, QTableWidget, QComboBox {{ background: rgba(1,8,12,220); border: 1px solid rgba(0,217,245,55); }}
"""


def _theme_path(name):
    return Path(RESOURCE_DIR) / "gui" / "themes" / name


def theme_stylesheet(reduced_motion=False):
    try:
        base = _theme_path("cinematic.qss").read_text(encoding="utf-8")
    except OSError:
        base = FALLBACK_QSS
    if reduced_motion:
        try:
            base += "\n" + _theme_path("reduced_motion.qss").read_text(encoding="utf-8")
        except OSError:
            pass
    return base


APP_QSS = theme_stylesheet(False)
