# 🚗 CustomGauge Dashboard (PySide6)

<img width="1252" height="469" alt="image" src="https://github.com/user-attachments/assets/dcc18a72-e95b-4fda-a72f-650ebbe87803" />
**CustomGauge** is a fully customizable PySide6 widget for building beautiful dashboards with gauges — perfect for automotive-style UIs, monitoring panels, or any real-time visualization of values.

---

## ✨ Features

- 🎨 **Customizable Appearance**  
  - Colors for dial, needle, ticks, labels, and text.  
  - Flexible sizing and label spacing.  

- ⚡ **Rich Configuration**  
  - Define min/max values, major/minor ticks, and angles.  
  - Add labels, units, and bottom text.  
  - Optional **needle toggle** for minimalist gauges.  

- 📟 **Special Add-ons**  
  - Built-in support for **Odometer** style display.  
  - Works seamlessly with layouts (Grid, HBox, VBox).  

---

## 📦 Installation

```bash
pip install PySide6

---

## 📚 API Overview

| Parameter       | Type        | Description                               |
| --------------- | ----------- | ----------------------------------------- |
| `label`         | `str`       | Main label (e.g., "RPM", "FUEL")          |
| `units`         | `str`       | Units shown (e.g., "PSI", "°F")           |
| `min_value`     | `int/float` | Minimum gauge value                       |
| `max_value`     | `int/float` | Maximum gauge value                       |
| `major_tick`    | `int/float` | Step for major ticks                      |
| `minor_tick`    | `int/float` | Step for minor ticks                      |
| `start_angle`   | `int`       | Starting angle (degrees)                  |
| `end_angle`     | `int`       | Ending angle (degrees)                    |
| `needle_color`  | `QColor`    | Needle color                              |
| `dial_color`    | `QColor`    | Dial arc color                            |
| `label_spacing` | `float`     | Adjust spacing between dial and labels    |
| `odometer`      | `bool`      | Enable odometer display (for speedometer) |
| `needle`        | `bool`      | Show or hide the needle                   |

---

## 🛠️ Quick Start Demo (Full Dashboard)

```python
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
    sys.exit(app.exec())```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the issues page
 or submit a pull request.

If you’d like to:

Fix bugs 🐛

Improve performance ⚡

Add new features 🎉

Enhance documentation 📖

… we’d love your input!

---

## 🔮 Future Enhancements

⏱️ Real-time updates from sensors or APIs

🌀 Animated needle movement for smooth transitions

🌈 Themes & presets (dark mode, automotive, sci-fi)

📊 Data bindings (connect gauges directly to live values)

🖥️ Demo app with multiple dashboard layouts

