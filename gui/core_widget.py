"""
Animated assistant core - layered circular system display with rotating
rings, voice-activity pulses, a scanning line and a state-driven glow.

Original procedural design (QPainter); no external artwork. Frame rate is
capped and animation can be reduced/disabled for low-power systems.
"""
import math

from PySide6.QtCore import Qt, QTimer, QRectF, Property
from PySide6.QtGui import QPainter, QPen, QColor, QRadialGradient, QBrush, QFont
from PySide6.QtWidgets import QWidget

from gui import styles


class ReactorCore(QWidget):
    """Central animated core. set_state() drives colour + motion."""

    STATE_COLORS = {
        "idle": QColor(styles.TEXT_DIM),
        "loading": QColor(styles.AMBER),
        "listening_wake": QColor(styles.CYAN),
        "wake_detected": QColor(styles.CYAN_GLOW),
        "recording": QColor(styles.CYAN_GLOW),
        "processing": QColor(styles.AMBER),
        "planning": QColor(styles.AMBER),
        "executing": QColor(styles.CYAN_GLOW),
        "speaking": QColor(styles.BLUE_WHITE),
        "ready": QColor(styles.CYAN),
        "error": QColor(styles.DANGER),
        "failure": QColor(styles.DANGER),
        "recovery": QColor(styles.AMBER),
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(320, 320)
        self._angle1 = 0.0
        self._angle2 = 180.0
        self._angle3 = 90.0
        self._pulse = 0.0          # 0..1 voice activity pulse
        self._scan = 0.0
        self._level = 0.0          # real audio waveform level
        self._state = "idle"
        self._reduce_motion = False
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(100)     # low-cost idle cadence
        self._phase = 0.0

    # ------------------------------------------------------------------ api
    def set_state(self, state):
        self._state = state
        active = state in ("listening_wake", "recording", "processing",
                           "planning", "executing", "wake_detected", "speaking")
        self._timer.setInterval(250 if self._reduce_motion else (16 if active else 100))
        if state == "wake_detected":
            self.trigger_pulse()
        self.update()

    def set_reduce_motion(self, on):
        self._reduce_motion = bool(on)
        self.set_state(self._state)

    def trigger_pulse(self):
        self._pulse = 1.0

    def set_level(self, value):
        """Feed a 0..1 audio level for the waveform ring."""
        self._level = max(0.0, min(1.0, float(value)))

    # ------------------------------------------------------------------ anim
    def _tick(self):
        speed = 0.0 if self._reduce_motion else 1.0
        busy = self._state in ("listening_wake", "recording", "processing",
                               "wake_detected", "speaking")
        mult = 2.2 if busy else 0.6
        self._angle1 = (self._angle1 + 0.9 * mult * speed) % 360
        self._angle2 = (self._angle2 - 0.6 * mult * speed) % 360
        self._angle3 = (self._angle3 + 1.4 * mult * speed) % 360
        self._scan = (self._scan + (1.6 * mult * speed)) % 360
        self._phase += 0.12 * mult * speed
        if self._pulse > 0:
            self._pulse = max(0.0, self._pulse - 0.03)
        if not busy:
            self._level *= 0.85
        self.update()

    # ------------------------------------------------------------------ paint
    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w / 2.0, h / 2.0
        radius = min(w, h) / 2.0 - 16

        color = self.STATE_COLORS.get(self._state, QColor(styles.CYAN))

        # --- core glow ----------------------------------------------------
        glow_r = radius * (0.42 + 0.06 * math.sin(self._phase) + 0.18 * self._pulse)
        grad = QRadialGradient(cx, cy, max(glow_r, 1.0))
        c = QColor(color)
        c.setAlpha(200 if self._state != "idle" else 90)
        grad.setColorAt(0.0, c)
        c2 = QColor(color)
        c2.setAlpha(40)
        grad.setColorAt(0.7, c2)
        grad.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(cx - glow_r, cy - glow_r, glow_r * 2, glow_r * 2))

        # --- waveform ring (voice activity) -------------------------------
        bars = 64
        base = radius * 0.55
        pen = QPen(QColor(color))
        pen.setWidth(2)
        painter.setPen(pen)
        for i in range(bars):
            frac = i / bars
            ang = frac * 2 * math.pi
            wobble = math.sin(self._phase * 2 + i * 0.5) * self._level * radius * 0.10
            r1 = base
            r2 = base + 6 + abs(wobble) + self._pulse * 10
            x1 = cx + math.cos(ang) * r1
            y1 = cy + math.sin(ang) * r1
            x2 = cx + math.cos(ang) * r2
            y2 = cy + math.sin(ang) * r2
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        # --- rotating rings ----------------------------------------------
        self._ring(painter, cx, cy, radius * 0.78, self._angle1, 100, color, 3)
        self._ring(painter, cx, cy, radius * 0.88, self._angle2, 60, color, 2)
        self._ring(painter, cx, cy, radius * 0.70, self._angle3, 140, color, 2)

        # --- outer frame circle ------------------------------------------
        frame = QColor(styles.CYAN)
        frame.setAlpha(60)
        painter.setPen(QPen(frame, 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QRectF(cx - radius, cy - radius, radius * 2, radius * 2))

        # --- scanning line -------------------------------------------------
        if not self._reduce_motion:
            scan_pen = QPen(QColor(color))
            scan_pen.setWidth(1)
            scan_c = QColor(color)
            scan_c.setAlpha(120)
            scan_pen.setColor(scan_c)
            painter.setPen(scan_pen)
            ang = math.radians(self._scan)
            painter.drawLine(int(cx), int(cy),
                             int(cx + math.cos(ang) * radius),
                             int(cy + math.sin(ang) * radius))

        # --- center label --------------------------------------------------
        painter.setPen(QPen(QColor(styles.TEXT)))
        font = QFont("Consolas", 10)
        font.setLetterSpacing(QFont.PercentageSpacing, 110)
        painter.setFont(font)
        label = self._state.replace("_", " ").upper()
        painter.drawText(QRectF(cx - radius, cy - 10, radius * 2, 20),
                         Qt.AlignCenter, label)

        painter.end()

    def _ring(self, painter, cx, cy, r, start_angle, span, color, width):
        pen = QPen(QColor(color))
        pen.setWidth(width)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        rect = QRectF(cx - r, cy - r, r * 2, r * 2)
        # draw two arcs for a layered look
        painter.drawArc(rect, int(start_angle * 16), int(span * 16))
        painter.drawArc(rect, int((start_angle + 180) * 16), int(span * 16))
