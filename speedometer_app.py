import json
import os
import sys
import math
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QDialog, QLabel,
    QPushButton, QLineEdit, QCheckBox
)
from PySide6.QtGui import QPainter, QPen, QFont, QColor, QPolygonF
from PySide6.QtCore import QPoint, Qt, QRectF, QPointF, QTimer

from CustomGauge import CustomGauge, AlertIcon, TurnSignal

POSITIONS_FILE = "gauge_positions.json"

# ===================== Draggable Wrapper =====================
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


# ===================== Save/Load =====================
def save_positions_and_scales(widgets, scales):
    positions = {w.name: [w.x(), w.y()] for w in widgets}
    data = {"positions": positions, "scales": scales}
    with open(POSITIONS_FILE, "w") as f:
        json.dump(data, f)

def load_positions_and_scales():
    if os.path.exists(POSITIONS_FILE):
        with open(POSITIONS_FILE, "r") as f:
            return json.load(f)
    return None


# ===================== Setup Dialog =====================
class DashboardSetupDialog(QDialog):
    def __init__(self, widgets, scales, alerts, signals, parent=None):
        super().__init__(parent)
        self.widgets = widgets
        self.scales = scales
        self.alerts = alerts
        self.signals = signals
        self.selected_idx = 0

        self.setWindowTitle("Dashboard Setup")
        self.setMinimumWidth(400)

        self.default_sizes = [w.width() for w in widgets]
        self.scale_factors = [
            1.0 if scales.get(w.name, None) is None else scales.get(w.name) / self.default_sizes[i]
            for i, w in enumerate(widgets)
        ]

        # --- Gauge scale controls ---
        self.label = QLabel(f"Selected: {widgets[0].name}")
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

        scale_layout = QHBoxLayout()
        scale_layout.addWidget(self.decrease_btn)
        scale_layout.addWidget(self.scale_label)
        scale_layout.addWidget(self.increase_btn)
        scale_layout.addWidget(self.custom_input)
        scale_layout.addWidget(self.custom_box)
        scale_layout.addWidget(self.apply_btn)

        # --- Navigation ---
        self.prev_btn = QPushButton("Previous")
        self.next_btn = QPushButton("Next")
        self.ok_btn = QPushButton("OK")

        self.prev_btn.clicked.connect(self.prev_widget)
        self.next_btn.clicked.connect(self.next_widget)
        self.ok_btn.clicked.connect(self.accept)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)
        nav_layout.addWidget(self.ok_btn)

        # --- Alerts checkboxes ---
        self.alert_checks = {}
        for name, alert in alerts.items():
            cb = QCheckBox(f"{name.upper()}")
            cb.setChecked(alert.active)
            cb.stateChanged.connect(lambda state, a=alert: a.set_active(bool(state)))
            self.alert_checks[name] = cb

        alerts_layout = QVBoxLayout()
        alerts_layout.addWidget(QLabel("Alerts:"))
        for cb in self.alert_checks.values():
            alerts_layout.addWidget(cb)

        # --- Signals checkboxes ---
        self.signal_checks = {}
        for name, signal in signals.items():
            cb = QCheckBox(f"{name.upper()} SIGNAL")
            cb.setChecked(signal.on)
            cb.stateChanged.connect(lambda state, s=signal: s.start() if state else s.stop())
            self.signal_checks[name] = cb

        signals_layout = QVBoxLayout()
        signals_layout.addWidget(QLabel("Turn Signals:"))
        for cb in self.signal_checks.values():
            signals_layout.addWidget(cb)

        # --- Final layout ---
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addLayout(scale_layout)
        layout.addLayout(nav_layout)
        layout.addLayout(alerts_layout)
        layout.addLayout(signals_layout)

        self.update_ui()

    def set_widget_size(self, idx):
        factor = self.scale_factors[idx]
        base = self.default_sizes[idx]
        size = int(base * factor)
        self.widgets[idx].widget.setFixedSize(size, size)
        self.widgets[idx].setFixedSize(size, size)
        self.scales[self.widgets[idx].name] = size

    def decrease_scale(self):
        idx = self.selected_idx
        self.scale_factors[idx] = max(0.1, self.scale_factors[idx] - 0.1)
        self.set_widget_size(idx)
        self.update_ui()

    def increase_scale(self):
        idx = self.selected_idx
        self.scale_factors[idx] += 0.1
        self.set_widget_size(idx)
        self.update_ui()

    def apply_custom_scale(self):
        idx = self.selected_idx
        try:
            val = float(self.custom_box.text())
            if val > 0:
                self.scale_factors[idx] = val
                self.set_widget_size(idx)
                self.update_ui()
        except ValueError:
            pass

    def prev_widget(self):
        self.selected_idx = (self.selected_idx - 1) % len(self.widgets)
        self.update_ui()

    def next_widget(self):
        self.selected_idx = (self.selected_idx + 1) % len(self.widgets)
        self.update_ui()

    def update_ui(self):
        idx = self.selected_idx
        w = self.widgets[idx]
        self.label.setText(f"Selected: {w.name}")
        self.scale_label.setText(f"Scale Factor: {self.scale_factors[idx]:.1f}")
        self.custom_box.setText("")


# ===================== Main =====================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.setGeometry(100, 100, 1200, 500)
    window.setWindowTitle("Draggable Gauges + Turn Signals")

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
    # Add dashboard alert icons
    alerts = {
        "check_engine": AlertIcon("icons/check_engine.png", "ENGINE"),
        "oil": AlertIcon("icons\oil.png", "OIL"),
        "abs": AlertIcon("icons/abs.png", "ABS"),
    }

    scales = {}
    for name, gauge, default_size in gauge_defs:
        size = default_size
        if setup_data and "scales" in setup_data and name in setup_data["scales"]:
            size = setup_data["scales"][name]
        gauge.setFixedSize(size, size)
        dg = DraggableGauge(gauge, name, draggable)
        dg.setParent(window)
        gauges.append(dg)
        scales[name] = size
        
    for name, widget in alerts.items():
        dg = DraggableGauge(widget, name, draggable)
        dg.setParent(window)
        gauges.append(dg)   # include in same list for saving
        scales[name] = widget.width()

    # Add turn signals
    signal_defs = [
        ("LEFT_SIGNAL", TurnSignal("left"), 60),
        ("RIGHT_SIGNAL", TurnSignal("right"), 60),
    ]

    for name, signal, default_size in signal_defs:
        size = default_size
        if setup_data and "scales" in setup_data and name in setup_data["scales"]:
            size = setup_data["scales"][name]
        signal.setFixedSize(size, size)
        dg = DraggableGauge(signal, name, draggable)
        dg.setParent(window)
        gauges.append(dg)
        scales[name] = size

    # Default positions
    default_positions = [
        (20, 20), (240, 20), (20, 240), (240, 240), (500, 60), (950, 60),  # gauges
        (850, 20), (1050, 20),  # turn signals
        (700, 350), (770, 350), (840, 350),  # alert icons
    ]
  
    if setup_data and "positions" in setup_data:
        for g in gauges:
            pos = setup_data["positions"].get(g.name,
                                              default_positions[gauges.index(g)])
            g.move(pos[0], pos[1])
    else:
        for g, pos in zip(gauges, default_positions):
            g.move(pos[0], pos[1])


    left_signal = next((g.gauge for g in gauges if g.name == "LEFT_SIGNAL"), None)
    right_signal = next((g.gauge for g in gauges if g.name == "RIGHT_SIGNAL"), None)

    # Keyboard controls for signals
    def keyPressEvent(event):
        

        if event.key() == Qt.Key_A and left_signal:
            if left_signal.on:
                left_signal.stop()
            else:
                left_signal.start()
        elif event.key() == Qt.Key_D and right_signal:
            if right_signal.on:
                right_signal.stop()
            else:
                right_signal.start()
                
    alerts["check_engine"].set_active(True)
    alerts["oil"].set_active(False)
    alerts["abs"].set_active(True)

    window.keyPressEvent = keyPressEvent

    window.show()

    if draggable:
        setup_dialog = DashboardSetupDialog(gauges, scales, alerts, {"left": left_signal, "right": right_signal})
        setup_dialog.setWindowModality(Qt.NonModal)
        setup_dialog.show()


    def on_close():
        if draggable:
            save_positions_and_scales(gauges, scales)

    app.aboutToQuit.connect(on_close)
    sys.exit(app.exec())
