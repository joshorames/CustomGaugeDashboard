from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPainter, QPen, QFont, QColor, QPolygonF, QPixmap
from PySide6.QtCore import Qt, QRectF, QPointF, QPoint
import sys
import math
from PySide6.QtCore import QTimer


class CustomGauge(QWidget):
    def __init__(
        self,
        needle=True,
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
        parent=None,
        odometer=False,
        bottom_text_size=14,
        label_size=16,
        value_size=16,
        label_spacing=0.65,
        odometer_font_size=16,
        fuel_ticks=False
    ):
        """_summary_

        Args:
            min_value (int, optional): _description_. Defaults to 0.
            max_value (int, optional): _description_. Defaults to 120.
            major_tick (int, optional): _description_. Defaults to 10.
            minor_tick (int, optional): _description_. Defaults to 5.
            label (str, optional): _description_. Defaults to "MPH\nkm/h".
            units (str, optional): _description_. Defaults to "MPH".
            needle_color (_type_, optional): _description_. Defaults to QColor("orange").
            dial_color (_type_, optional): _description_. Defaults to QColor("orange").
            start_angle (int, optional): _description_. Defaults to 210.
        """
        super().__init__(parent)
        self.needle = needle
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
        self.odometer = odometer
        self.bottom_text_size = bottom_text_size 
        self.label_size = label_size
        self.value_size = value_size
        self.label_spacing = label_spacing
        self.odometer_font_size = odometer_font_size
        self.fuel_ticks = fuel_ticks

    def set_value(self, value):
        """_summary_

        Args:
            value (_type_): _description_
        """
        self.value = max(self.min_value, min(value, self.max_value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 2 * 0.95  # 95% of half the smallest dimension

        # Draw black background
        painter.setBrush(Qt.black)
        painter.setPen(Qt.black)
        painter.drawEllipse(center, radius, radius)

        # Undo text size scaling: use fixed font sizes
   
        painter.setFont(QFont("Arial", self.value_size, QFont.Bold))
        number_offset = radius * self.label_spacing  # Move numbers further inward
        text_box = 32                  # Increase bounding box
       
        tick_outer = radius
        tick_inner = radius * 0.85
        minor_tick_inner = radius * 0.92

        sweep = self.start_angle - self.end_angle
        value_range = self.max_value - self.min_value
        for i in range(self.min_value, self.max_value + 1, self.minor_tick):
            angle = self.start_angle - ((i - self.min_value) * sweep / value_range)
            rad = math.radians(angle)
            x1 = center.x() + tick_inner * math.cos(rad)
            y1 = center.y() - tick_inner * math.sin(rad)
            x2 = center.x() + tick_outer * math.cos(rad)
            y2 = center.y() - tick_outer * math.sin(rad)

            # Major ticks and numbers
            if i % self.major_tick == 0:
                painter.setPen(QPen(Qt.white, max(2, int(radius * 0.03))))
                painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
                tx = center.x() + number_offset * math.cos(rad)
                ty = center.y() - number_offset * math.sin(rad)
                painter.setPen(Qt.white)
                if self.fuel_ticks:
                    if i == self.min_value:
                        painter.drawText(QRectF(tx-text_box/2, ty-text_box/2, text_box, text_box), Qt.AlignCenter, "E")
                    elif i == self.max_value:   
                        painter.drawText(QRectF(tx-text_box/2, ty-text_box/2, text_box, text_box), Qt.AlignCenter, "F")
                else:
                    painter.drawText(QRectF(tx-text_box/2, ty-text_box/2, text_box, text_box), Qt.AlignCenter, str(i))
            # Minor ticks
            else:
                painter.setPen(QPen(Qt.gray, max(1, int(radius * 0.015))))
                painter.drawLine(QPointF(x1, y1), QPointF(center.x() + minor_tick_inner * math.cos(rad), center.y() - minor_tick_inner * math.sin(rad)))

        # Draw needle
        if self.needle == True:
            needle_length = radius * 0.75
            needle_angle = self.start_angle - ((self.value - self.min_value) * sweep / value_range)
            rad = math.radians(needle_angle)
            nx = center.x() + needle_length * math.cos(rad)
            ny = center.y() - needle_length * math.sin(rad)
            painter.setPen(QPen(self.needle_color, max(6, int(radius * 0.05))))
            painter.drawLine(center, QPointF(nx, ny))

            # Draw center dial piece
            dial_radius = radius * 0.09
            painter.setPen(self.dial_color)
            painter.setBrush(self.dial_color)
            painter.drawEllipse(center, dial_radius, dial_radius)

        # Draw label
        painter.setFont(QFont("Arial", self.label_size, QFont.Bold))
        painter.setPen(Qt.white)
        painter.drawText(QRectF(center.x()-radius*0.25, center.y()-radius*0.25, radius*0.5, radius*0.18), Qt.AlignCenter, self.label)

        # Draw odometer rectangle (optional, static)
        odo_w = radius * 0.6
        odo_h = radius * 0.13
        if self.odometer == True:
            odo_rect = QRectF(center.x()-odo_w/2, center.y()+radius*0.35, odo_w, odo_h)
            painter.setPen(Qt.white)
            painter.setBrush(Qt.black)
            painter.drawRect(odo_rect)
            painter.setFont(QFont("Consolas", self.odometer_font_size, QFont.Bold))
            painter.drawText(odo_rect, Qt.AlignCenter, "000000")

        # Draw value text (below odometer)
        painter.setFont(QFont("Arial", self.bottom_text_size, QFont.Bold))
        painter.setPen(Qt.white)
        painter.drawText(QRectF(center.x()-odo_w/2, center.y()+radius*0.5, odo_w, odo_h), Qt.AlignCenter, f"{self.value} {self.units}")

class TurnSignal(QWidget):
    def __init__(self, direction="left", color="green", parent=None):
        super().__init__(parent)
        self.direction = direction
        self.color = QColor(color)
        self.on = False
        self.visible_state = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle)
        self.setFixedSize(60, 60)

    def start(self):
        self.on = True
        self.timer.start(500)  # blink every 500ms
        self.update()

    def stop(self):
        self.on = False
        self.visible_state = False
        self.timer.stop()
        self.update()

    def toggle(self):
        self.visible_state = not self.visible_state
        self.update()

    def paintEvent(self, event):
        if not self.on or not self.visible_state:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.color)
        painter.setPen(Qt.NoPen)

        w, h = self.width(), self.height()
        if self.direction == "left":
            points = [QPointF(w*0.8, h*0.2), QPointF(w*0.2, h*0.5), QPointF(w*0.8, h*0.8)]
        else:
            points = [QPointF(w*0.2, h*0.2), QPointF(w*0.8, h*0.5), QPointF(w*0.2, h*0.8)]
        painter.drawPolygon(QPolygonF(points))
        
class AlertIcon(QWidget):
    def __init__(self, icon_path, label="", active_color="red", inactive_color="gray", parent=None):
        super().__init__(parent)
        # Load the icon as is (transparent background)
        self.base_icon = QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label = label
        self.active_color = QColor(active_color)
        self.inactive_color = QColor(inactive_color)
        self.active = False
        self.setFixedSize(50, 60)

    def set_active(self, state: bool):
        self.active = state
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw a background circle to indicate state
        radius = 20
        center = QPoint(25, 25)
        color = self.active_color if self.active else self.inactive_color
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, radius, radius)

        # Draw the icon on top
        painter.drawPixmap(5, 5, self.base_icon)

        # Draw label under icon
        if self.label:
            painter.setPen(Qt.white)
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            painter.drawText(QRectF(0, 45, 50, 15), Qt.AlignCenter, self.label)
