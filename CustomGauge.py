from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPainter, QPen, QFont, QColor, QPolygonF, QPixmap, QImage
from PySide6.QtCore import Qt, QRectF, QPointF, QPoint
import sys
import math
from PySide6.QtCore import QTimer


class CustomGauge(QWidget):
    """A customizable gauge widget with needle, ticks, labels, and optional odometer."""
    def __init__(
        self,
        # Determine if needle is rendered or not
        needle=True,
        # Min value of the gauge
        min_value=0,
        # Max value of the gauge
        max_value=120,
        # Number of major ticks
        major_tick=10,
        # Number of minor ticks
        minor_tick=5,
        # Label text (can include \n for multi-line)
        label="MPH\nkm/h",
        # Units text (displayed below value)
        units="MPH",
        # Needle color
        needle_color=QColor("orange"),
        # Dial center color
        dial_color=QColor("orange"),
        # Start angle of the gauge (in degrees)
        start_angle=210,  
        # End angle of the gauge (in degrees)   
        end_angle=-30,       
        # Optional parent widget 
        parent=None,
        # Optional odometer display below the gauge
        odometer=False,
        # Bottom text size (value + units)
        bottom_text_size=14,
        # Label text size
        label_size=16,
        # Value text size
        value_size=16,
        # Spacing factor for label numbers (0.0 to 1.0, where 1.0 is at the edge)
        label_spacing=0.65,
        # Odometer font size
        odometer_font_size=16,
        # Use E and F for fuel gauge instead of 0 and max_value
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
            value (integer): Value to set the gauge to
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
    """A blinking turn signal arrow widget."""
    def __init__(self, direction="left", color="green", parent=None):
        """_summary_

        Args:
            direction (str, optional): Direction the arrow faces. Defaults to "left".
            color (str, optional): color of the arrow signal. Defaults to "green".
            parent (any, optional): parent object of arrow. Defaults to None.
        """
        super().__init__(parent)
        self.direction = direction
        self.color = QColor(color)
        self.on = False
        self.visible_state = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle)
        self.setFixedSize(60, 60)

    def start(self):
        """Start blinking the turn signal."""
        self.on = True
        self.timer.start(500)  # blink every 500ms
        self.update()

    def stop(self):
        """Stop blinking the turn signal."""
        self.on = False
        self.visible_state = False
        self.timer.stop()
        self.update()

    def toggle(self):
        """Toggle the visibility state of the turn signal."""
        self.visible_state = not self.visible_state
        self.update()

    def paintEvent(self, event):
        """Render the turn signal arrow if it's on and visible."""
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
        
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPixmap, QColor, QFont, QImage
from PySide6.QtCore import Qt, QRectF

class AlertIcon(QWidget):
    """A dashboard alert icon with active/inactive states."""
    def __init__(self, icon_path, label="", active_color="red", inactive_color="gray", parent=None):
        """_summary_

        Args:
            icon_path (str): path at which icon image is located. Defaults to "".
            label (str, optional): Label under the icon. Defaults to "".
            active_color (str, optional): Color the icon turns when active. Defaults to "red".
            inactive_color (str, optional): Color the icon turns when inactive. Defaults to "gray".
            parent (any, optional): Parent object. Defaults to None.
        """
        super().__init__(parent)
        self.icon_path = icon_path
        self.label = label
        self.active_color = QColor(active_color)
        self.inactive_color = QColor(inactive_color)

        self.base_icon = QPixmap(icon_path).scaled(
            40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        if self.base_icon.isNull():
            print(f"⚠️ Could not load icon: {icon_path}")

        self.active = False
        self.setFixedSize(50, 65)

        # Precompute both versions
        self.colored_active = self.colorize_icon(self.base_icon, self.active_color)
        self.colored_inactive = self.colorize_icon(self.base_icon, self.inactive_color)

    def set_active(self, state: bool):
        """Set the active state of the icon."""
        self.active = state
        self.update()

    def colorize_icon(self, pixmap: QPixmap, color: QColor) -> QPixmap:
        """Recolor only the symbol (non-transparent) pixels of the pixmap"""
        img = pixmap.toImage().convertToFormat(QImage.Format_ARGB32)

        for y in range(img.height()):
            for x in range(img.width()):
                pixel = img.pixelColor(x, y)
                if pixel.alpha() > 0:  # Only recolor the symbol pixels
                    new = QColor(color)
                    new.setAlpha(pixel.alpha())  # preserve alpha channel
                    img.setPixelColor(x, y, new)

        return QPixmap.fromImage(img)

    def paintEvent(self, event):
        """Render the icon with appropriate color and label."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        icon = self.colored_active if self.active else self.colored_inactive
        painter.drawPixmap(5, 5, icon)

        # Draw label under the icon
        if self.label:
            painter.setPen(Qt.white)
            painter.setFont(QFont("Arial", 9, QFont.Bold))
            painter.drawText(QRectF(0, 47, 50, 15), Qt.AlignCenter, self.label)