import json
import os
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QDialog, QLabel, QSlider, QPushButton, QLineEdit
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

def save_positions_and_scales(gauges, scales):
    positions = {g.name: [g.x(), g.y()] for g in gauges}
    data = {"positions": positions, "scales": scales}
    with open(POSITIONS_FILE, "w") as f:
        json.dump(data, f)

def load_positions_and_scales():
    if os.path.exists(POSITIONS_FILE):
        with open(POSITIONS_FILE, "r") as f:
            return json.load(f)
    return None

class GaugeSetupDialog(QDialog):
    def __init__(self, gauges, scales, parent=None):
        super().__init__(parent)
        self.gauges = gauges
        self.scales = scales
        self.selected_idx = 0
        self.setWindowTitle("Gauge Setup: Resize Gauges")
        self.setMinimumWidth(350)

        self.default_sizes = [g.width() for g in gauges]
        self.scale_factors = [1.0 if scales.get(g.name, None) is None else scales.get(g.name) / self.default_sizes[i] for i, g in enumerate(gauges)]

        self.label = QLabel(f"Selected Gauge: {gauges[0].name}")
        self.scale_label = QLabel(f"Scale Factor: {self.scale_factors[0]:.1f}")

        self.decrease_btn = QPushButton("-")
        self.increase_btn = QPushButton("+")
        self.custom_input = QLabel("Custom:")
        self.custom_box = QLineEdit()
        self.custom_box.setPlaceholderText("Enter scale (e.g. 1.2)")
        self.apply_btn = QPushButton("Apply")

        self.decrease_btn.clicked.connect(self.decrease_scale)
        self.increase_btn.clicked.connect(self.increase_scale)
        self.apply_btn.clicked.connect(self.apply_custom_scale)

        self.prev_btn = QPushButton("Previous")
        self.next_btn = QPushButton("Next")
        self.ok_btn = QPushButton("OK")
        self.prev_btn.clicked.connect(self.prev_gauge)
        self.next_btn.clicked.connect(self.next_gauge)
        self.ok_btn.clicked.connect(self.accept)

        scale_layout = QHBoxLayout()
        scale_layout.addWidget(self.decrease_btn)
        scale_layout.addWidget(self.scale_label)
        scale_layout.addWidget(self.increase_btn)
        scale_layout.addWidget(self.custom_input)
        scale_layout.addWidget(self.custom_box)
        scale_layout.addWidget(self.apply_btn)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.prev_btn)
        btn_layout.addWidget(self.next_btn)
        btn_layout.addWidget(self.ok_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addLayout(scale_layout)
        layout.addLayout(btn_layout)

        self.update_ui()

    def set_gauge_size(self, idx):
        factor = self.scale_factors[idx]
        base = self.default_sizes[idx]
        size = int(base * factor)
        self.gauges[idx].gauge.setFixedSize(size, size)  # Resize the gauge widget
        self.gauges[idx].setFixedSize(size, size)        # Resize the container
        self.scales[self.gauges[idx].name] = size

    def decrease_scale(self):
        idx = self.selected_idx
        self.scale_factors[idx] = max(0.1, self.scale_factors[idx] - 0.1)
        self.set_gauge_size(idx)
        self.update_ui()

    def increase_scale(self):
        idx = self.selected_idx
        self.scale_factors[idx] += 0.1
        self.set_gauge_size(idx)
        self.update_ui()

    def apply_custom_scale(self):
        idx = self.selected_idx
        try:
            val = float(self.custom_box.text())
            if val > 0:
                self.scale_factors[idx] = val
                self.set_gauge_size(idx)
                self.update_ui()
        except ValueError:
            pass  # Ignore invalid input

    def prev_gauge(self):
        self.selected_idx = (self.selected_idx - 1) % len(self.gauges)
        self.update_ui()

    def next_gauge(self):
        self.selected_idx = (self.selected_idx + 1) % len(self.gauges)
        self.update_ui()

    def update_ui(self):
        idx = self.selected_idx
        g = self.gauges[idx]
        self.label.setText(f"Selected Gauge: {g.name}")
        self.scale_label.setText(f"Scale Factor: {self.scale_factors[idx]:.1f}")
        self.custom_box.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.setGeometry(100, 100, 1200, 500)
    window.setWindowTitle("Draggable Gauges")

    setup_data = load_positions_and_scales()
    draggable = setup_data is None

    gauges = []
    gauge_defs = [
        ("OIL", CustomGauge(label="OIL", units="PSI", needle_color=QColor("red"), dial_color=QColor("red"), min_value=0, max_value=100, major_tick=25, minor_tick=5, start_angle=210, end_angle=-30), 200),
        ("WATER", CustomGauge(label="WATER", units="°F", needle_color=QColor("red"), dial_color=QColor("red"), min_value=100, max_value=250, major_tick=50, minor_tick=10, start_angle=210, end_angle=-30), 200),
        ("VOLTS", CustomGauge(label="VOLTS", units="V", needle_color=QColor("red"), dial_color=QColor("red"), min_value=8, max_value=18, major_tick=2, minor_tick=1, start_angle=210, end_angle=-30), 200),
        ("FUEL", CustomGauge(label="FUEL", units="F", needle_color=QColor("red"), dial_color=QColor("red"), min_value=0, max_value=10, major_tick=10, minor_tick=1, start_angle=210, end_angle=-30, fuel_ticks=True), 200),
        ("MPH", CustomGauge(label="MPH", units="MPH", needle_color=QColor("red"), dial_color=QColor("red"), min_value=0, max_value=160, major_tick=20, minor_tick=10, start_angle=210, end_angle=-30, odometer=True), 400),
        ("RPM", CustomGauge(label="RPM", units="x1000", needle_color=QColor("red"), dial_color=QColor("red"), min_value=0, max_value=10, major_tick=1, minor_tick=1, start_angle=210, end_angle=-30), 400),
    ]

    scales = {}
    for idx, (name, gauge, default_size) in enumerate(gauge_defs):
        size = default_size
        if setup_data and "scales" in setup_data and name in setup_data["scales"]:
            size = setup_data["scales"][name]
        gauge.setFixedSize(size, size)
        dg = DraggableGauge(gauge, name, draggable)
        dg.setParent(window)
        gauges.append(dg)
        scales[name] = size

    # Default positions (approximate layout)
    default_positions = [
        (20, 20), (240, 20), (20, 240), (240, 240), (500, 60), (950, 60)
    ]

    # Set positions
    if setup_data and "positions" in setup_data:
        for g in gauges:
            pos = setup_data["positions"].get(g.name, default_positions[gauges.index(g)])
            g.move(pos[0], pos[1])
    else:
        for g, pos in zip(gauges, default_positions):
            g.move(pos[0], pos[1])

    # Show main window first
    window.show()

    # Show setup dialog if draggable
    if draggable:
        setup_dialog = GaugeSetupDialog(gauges, scales)
        setup_dialog.setWindowModality(Qt.NonModal)  # Allow both windows to be visible and interactive
        setup_dialog.show()  # Use show() instead of exec()

    # Save positions and scales on close if draggable
    def on_close():
        if draggable:
            save_positions_and_scales(gauges, scales)

    app.aboutToQuit.connect(on_close)
    sys.exit(app.exec())