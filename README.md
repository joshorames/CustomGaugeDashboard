<img width="1252" height="469" alt="image" src="https://github.com/user-attachments/assets/dcc18a72-e95b-4fda-a72f-650ebbe87803" />
Example Usage:
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout
from PySide6.QtGui import QColor
import sys
from CustomGauge import CustomGauge


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    main_layout = QHBoxLayout(window)

    # Left: 2x2 grid of small gauges
    left_grid = QGridLayout()
    oil_gauge = CustomGauge(
        label="OIL",
        units="PSI",
        needle_color=QColor("red"),
        dial_color=QColor("red"),
        min_value=0,
        max_value=100,
        major_tick=25,
        minor_tick=5,
        start_angle=210,
        end_angle=-30,
        bottom_text_size=10,
        label_size=10,
        value_size=10,
        label_spacing=0.65,
        needle=False
    )
    oil_gauge.setFixedSize(200, 200)
    left_grid.addWidget(oil_gauge, 0, 0)

    water_gauge = CustomGauge(
        label="WATER",
        units="°F",
        needle_color=QColor("red"),
        dial_color=QColor("red"),
        min_value=100,
        max_value=250,
        major_tick=50,
        minor_tick=10,
        start_angle=210,
        end_angle=-30,
        bottom_text_size=10,
        label_size=10,
        value_size=10,
        label_spacing=0.65
    )
    water_gauge.setFixedSize(200, 200)
    left_grid.addWidget(water_gauge, 0, 1)

    volt_gauge = CustomGauge(
        label="VOLTS",
        units="V",
        needle_color=QColor("red"),
        dial_color=QColor("red"),
        min_value=8,
        max_value=18,
        major_tick=2,
        minor_tick=1,
        start_angle=210,
        end_angle=-30,
        bottom_text_size=10,
        label_size=10,
        value_size=10,
        label_spacing=0.65
    )
    volt_gauge.setFixedSize(200, 200)
    left_grid.addWidget(volt_gauge, 1, 0)

    fuel_gauge = CustomGauge(
        label="FUEL",
        units="F",
        needle_color=QColor("red"),
        dial_color=QColor("red"),
        min_value=0,
        max_value=1,
        major_tick=1,
        minor_tick=1,
        start_angle=210,
        end_angle=-30,
        bottom_text_size=10,
        label_size=10,
        value_size=10,
        label_spacing=0.65
    )
    fuel_gauge.setFixedSize(200, 200)
    left_grid.addWidget(fuel_gauge, 1, 1)

    main_layout.addLayout(left_grid)

    # Center: two large gauges side by side
    center_row = QHBoxLayout()
    speedometer = CustomGauge(
        label="MPH",
        units="MPH",
        needle_color=QColor("red"),
        dial_color=QColor("red"),
        min_value=0,
        max_value=160,
        major_tick=20,
        minor_tick=10,
        start_angle=210,
        end_angle=-30,
        odometer=True,
        label_spacing=0.70
    )
    speedometer.setFixedSize(400, 400)
    center_row.addWidget(speedometer)

    tachometer = CustomGauge(
        label="RPM",
        units="x1000",
        needle_color=QColor("red"),
        dial_color=QColor("red"),
        min_value=0,
        max_value=10,
        major_tick=1,
        minor_tick=1,
        start_angle=210,
        end_angle=-30,
        label_spacing=0.70
    )
    tachometer.setFixedSize(400, 400)
    center_row.addWidget(tachometer)

    main_layout.addLayout(center_row)

    window.setLayout(main_layout)
    window.show()
    sys.exit(app.exec())


