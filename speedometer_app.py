import json
import os
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout
from PySide6.QtGui import QColor, QMouseEvent
from PySide6.QtCore import QPoint, Qt
import sys
from CustomGauge import CustomGauge

POSITIONS_FILE = "gauge_positions.json"

class DraggableGauge(QWidget):
    def __init__(self, gauge, name, draggable=True, parent=None):
        super().__init__(parent)
        self.gauge = gauge
        self.name = name
        self.draggable = draggable
        self.offset = QPoint()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(gauge)
        self.setFixedSize(gauge.width(), gauge.height())

    def mousePressEvent(self, event):
        if self.draggable and event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & Qt.LeftButton:
            self.move(self.mapToParent(event.pos() - self.offset))

def save_positions(gauges):
    positions = {g.name: [g.x(), g.y()] for g in gauges}
    with open(POSITIONS_FILE, "w") as f:
        json.dump(positions, f)

def load_positions():
    if os.path.exists(POSITIONS_FILE):
        with open(POSITIONS_FILE, "r") as f:
            return json.load(f)
    return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.setGeometry(100, 100, 1200, 500)
    window.setWindowTitle("Draggable Gauges")

    positions = load_positions()
    draggable = positions is None

    gauges = []
    gauge_defs = [
        ("OIL", CustomGauge(label="OIL", units="PSI", needle_color=QColor("red"), dial_color=QColor("red"), min_value=0, max_value=100, major_tick=25, minor_tick=5, start_angle=210, end_angle=-30,bottom_text_size=10,label_size=10,value_size=10,label_spacing=0.65,), 200, 200),
        ("WATER", CustomGauge(label="WATER", units="°F", needle_color=QColor("red"), dial_color=QColor("red"), min_value=100, max_value=250, major_tick=50, minor_tick=10, start_angle=210, end_angle=-30,bottom_text_size=10,
        label_size=10,
        value_size=10,
        label_spacing=0.65), 200, 200),
        ("VOLTS", CustomGauge(label="VOLTS", units="V", needle_color=QColor("red"), dial_color=QColor("red"), min_value=8, max_value=18, major_tick=2, minor_tick=1, start_angle=210, end_angle=-30, bottom_text_size=10,
        label_size=10,
        value_size=10,
        label_spacing=0.65), 200, 200),
        ("FUEL", CustomGauge(label="FUEL", units="F", needle_color=QColor("red"), dial_color=QColor("red"), min_value=0, max_value=10, major_tick=10, minor_tick=1, start_angle=210, end_angle=-30,bottom_text_size=10,
        label_size=10,
        value_size=10,
        label_spacing=0.65, fuel_ticks=True), 200, 200),
        ("MPH", CustomGauge(label="MPH", units="MPH", needle_color=QColor("red"), dial_color=QColor("red"), min_value=0, max_value=160, major_tick=20, minor_tick=10, start_angle=210, end_angle=-30, odometer=True, label_spacing=0.70), 400, 400),
        ("RPM", CustomGauge(label="RPM", units="x1000", needle_color=QColor("red"), dial_color=QColor("red"), min_value=0, max_value=10, major_tick=1, minor_tick=1, start_angle=210, end_angle=-30,label_spacing=0.70), 400, 400),
    ]

    for idx, (name, gauge, w, h) in enumerate(gauge_defs):
        gauge.setFixedSize(w, h)
        dg = DraggableGauge(gauge, name, draggable)
        dg.setParent(window)
        gauges.append(dg)

    # Default positions (approximate layout)
    default_positions = [
        (20, 20), (240, 20), (20, 240), (240, 240), (500, 60), (950, 60)
    ]

    # Set positions
    if positions:
        for g in gauges:
            pos = positions.get(g.name, default_positions[gauges.index(g)])
            g.move(pos[0], pos[1])
    else:
        for g, pos in zip(gauges, default_positions):
            g.move(pos[0], pos[1])

    # Save positions on close if draggable
    def on_close():
        if draggable:
            save_positions(gauges)

    app.aboutToQuit.connect(on_close)
    window.show()
    sys.exit(app.exec())