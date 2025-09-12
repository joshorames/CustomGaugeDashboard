from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import QTimer
import sys
from CustomGauge import CustomGauge

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QHBoxLayout(window)

    # Speedometer gauge
    gauge1 = CustomGauge(
        label="SPEED",
        units="MPH",
        needle_color=QColor("orange"),
        dial_color=QColor("orange"),
        min_value=0,
        max_value=120,
        major_tick=10,
        minor_tick=5,
        start_angle=210,
        end_angle=-30
    )
    layout.addWidget(gauge1)

    # Tachometer gauge
    gauge2 = CustomGauge(
        label="TACH",
        units="RPM",
        needle_color=QColor("red"),
        dial_color=QColor("red"),
        min_value=0,
        max_value=8,
        major_tick=1,
        minor_tick=1,
        start_angle=210,
        end_angle=-30
    )
    layout.addWidget(gauge2)

    # Test value updates
    def update_value():
        gauge1.set_value((gauge1.value + 1) % 121)      # Speedometer: 0-120
        gauge2.set_value((gauge2.value + 1) % 9)   # Tachometer: 0-8000

    timer = QTimer()
    timer.timeout.connect(update_value)
    timer.start(100)  # Update value every 100 ms

    window.setLayout(layout)
    window.resize(900, 500)
    window.show()
    sys.exit(app.exec())