"""
System tray icon + menu.

Provides quick access to Open / Start Voice / Stop Voice / Mute / Logs /
Settings / Exit. Closing the main window minimizes here; only Exit fully
shuts the assistant down. The icon is drawn procedurally (no external art).
"""
from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen
from PySide6.QtWidgets import QSystemTrayIcon, QMenu

from gui import styles


def make_icon(size=64):
    """Procedural reactor-core icon (cyan rings on dark)."""
    pix = QPixmap(size, size)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)
    cx = cy = size / 2.0
    p.setPen(QPen(QColor(styles.CYAN), max(2, size // 16)))
    p.drawEllipse(int(cx - size * 0.32), int(cy - size * 0.32),
                  int(size * 0.64), int(size * 0.64))
    p.setPen(QPen(QColor(styles.CYAN_GLOW), max(2, size // 20)))
    r = size * 0.46
    p.drawArc(int(cx - r), int(cy - r), int(r * 2), int(r * 2), 30 * 16, 120 * 16)
    p.drawArc(int(cx - r), int(cy - r), int(r * 2), int(r * 2), 210 * 16, 120 * 16)
    p.end()
    return QIcon(pix)


class TrayIcon(QObject):
    openRequested = Signal()
    startVoiceRequested = Signal()
    stopVoiceRequested = Signal()
    muteRequested = Signal()
    logsRequested = Signal()
    settingsRequested = Signal()
    exitRequested = Signal()

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.tray = QSystemTrayIcon(make_icon(), app)
        self.menu = QMenu()
        self._add("Open JARVIS", self.openRequested)
        self.menu.addSeparator()
        self._add("Start Voice", self.startVoiceRequested)
        self._add("Stop Voice", self.stopVoiceRequested)
        self._add("Mute Speech", self.muteRequested)
        self.menu.addSeparator()
        self._add("Open Logs", self.logsRequested)
        self._add("Settings", self.settingsRequested)
        self.menu.addSeparator()
        self._add("Exit", self.exitRequested)
        self.tray.setContextMenu(self.menu)
        self.tray.setToolTip("JARVIS")
        self.tray.activated.connect(self._on_activate)

    def _add(self, label, signal):
        self.menu.addAction(label, signal.emit)

    def _on_activate(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.openRequested.emit()

    def show(self):
        self.tray.show()

    def notify(self, title, message):
        try:
            self.tray.showMessage(title, message, QSystemTrayIcon.Information, 3000)
        except Exception:
            pass

    def hide(self):
        self.tray.hide()