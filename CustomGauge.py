from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPainter, QPen, QFont, QColor
from PySide6.QtCore import Qt, QRectF, QPointF
import sys
import math
from PySide6.QtCore import QTimer

class CustomGauge(QWidget):
    def __init__(
        self,
        min_value=0,
        max_value=120,
        major_tick=10,
        minor_tick=5,
        label="MPH\nkm/h",
        units="MPH",
        needle_color=QColor("orange"),
        dial_color=QColor("orange"),
        start_angle=210,      # default sweep start
        end_angle=-30,        # default sweep end
        parent=None
    ):
        super().__init__(parent)
        self.value = min_value
        self.min_value = min_value
        self.max_value = max_value
        self.major_tick = major_tick
        self.minor_tick = minor_tick
        self.label = label
        self.units = units
        self.needle_color = needle_color
        self.dial_color = dial_color
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.setMinimumSize(400, 400)
        self.setWindowTitle("Custom Gauge")

    def set_value(self, value):
        self.value = max(self.min_value, min(value, self.max_value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 2 - 20

        # Draw black background
        painter.setBrush(Qt.black)
        painter.setPen(Qt.black)
        painter.drawEllipse(center, radius, radius)

        # Draw ticks and numbers
        # Use a smaller font and larger offset for tachometer
        if self.max_value > 1000:
            painter.setFont(QFont("Arial", 11, QFont.Bold))
            number_offset = 100
        else:
            painter.setFont(QFont("Arial", 14, QFont.Bold))
            number_offset = 60

        sweep = self.start_angle - self.end_angle
        value_range = self.max_value - self.min_value
        for i in range(self.min_value, self.max_value + 1, self.minor_tick):
            angle = self.start_angle - ((i - self.min_value) * sweep / value_range)
            rad = math.radians(angle)
            x1 = center.x() + (radius - 20) * math.cos(rad)
            y1 = center.y() - (radius - 20) * math.sin(rad)
            x2 = center.x() + radius * math.cos(rad)
            y2 = center.y() - radius * math.sin(rad)

            # Major ticks and numbers
            if i % self.major_tick == 0:
                painter.setPen(QPen(Qt.white, 3))
                painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
                tx = center.x() + (radius - number_offset) * math.cos(rad)
                ty = center.y() - (radius - number_offset) * math.sin(rad)
                painter.setPen(Qt.white)
                painter.drawText(QRectF(tx-18, ty-12, 36, 24), Qt.AlignCenter, str(i))
            # Minor ticks
            else:
                painter.setPen(QPen(Qt.gray, 1))
                painter.drawLine(QPointF(x1, y1), QPointF(x1 + 10 * math.cos(rad), y1 - 10 * math.sin(rad)))

        # Draw needle
        needle_angle = self.start_angle - ((self.value - self.min_value) * sweep / value_range)
        rad = math.radians(needle_angle)
        nx = center.x() + (radius - 50) * math.cos(rad)
        ny = center.y() - (radius - 50) * math.sin(rad)
        painter.setPen(QPen(self.needle_color, 8))
        painter.drawLine(center, QPointF(nx, ny))

        # Draw center dial piece
        painter.setPen(self.dial_color)
        painter.setBrush(self.dial_color)
        painter.drawEllipse(center, 18, 18)

        # Draw label
        painter.setFont(QFont("Arial", 18, QFont.Bold))
        painter.setPen(Qt.white)
        painter.drawText(QRectF(center.x()-50, center.y()-55, 100, 50), Qt.AlignCenter, self.label)

        # Draw odometer rectangle (optional, static)
        odo_rect = QRectF(center.x()-60, center.y()+radius//2-10, 120, 30)
        painter.setPen(Qt.white)
        painter.setBrush(Qt.black)
        painter.drawRect(odo_rect)
        painter.setFont(QFont("Consolas", 16, QFont.Bold))
        painter.drawText(odo_rect, Qt.AlignCenter, "000000")

        # Draw value text (below odometer)
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.setPen(Qt.white)
        painter.drawText(QRectF(center.x()-50, center.y()+radius//2+25, 100, 25), Qt.AlignCenter, f"{self.value} {self.units}")
