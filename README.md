# 🚗 CustomGauge Dashboard (PySide6)

<img width="1234" height="459" alt="image" src="https://github.com/user-attachments/assets/e03f0d74-01f7-4874-8d26-8c1751ac4b28" />
![Uploading image.png…]()

**CustomGauge** is a fully customizable PySide6 widget for building beautiful dashboards with gauges — perfect for automotive-style UIs, monitoring panels, or any real-time visualization of values.

---

## ✨ Features
- 🎨 Fully customizable colors, labels, and fonts  
- ⚡ Smooth, animated needle rendering  
- 📏 Configurable tick marks, angles, and scales  
- 🛠️ Support for **odometer display**
- ☝️ Dragging gauge support to place gauges at correct size for any application
- 📐 Easily integrate into PySide6 layouts (QHBox, QVBox, QGrid)  
- 💡 Create dashboards with multiple gauges  

---

## 📦 Installation

```bash
pip install PySide6
```

---

## 📚 API Overview

| Parameter          | Type        | Default | Description                              |
| ------------------ | ----------- | ------- | ---------------------------------------- |
| `label`            | `str`       | `""`    | Gauge label (e.g., RPM, MPH, FUEL)       |
| `units`            | `str`       | `""`    | Units displayed below the value          |
| `needle_color`     | `QColor`    | black   | Color of the needle                      |
| `dial_color`       | `QColor`    | gray    | Color of the dial arc                    |
| `min_value`        | `int/float` | 0       | Minimum scale value                      |
| `max_value`        | `int/float` | 100     | Maximum scale value                      |
| `major_tick`       | `int`       | 10      | Step between major ticks                 |
| `minor_tick`       | `int`       | 5       | Step between minor ticks                 |
| `start_angle`      | `int`       | 210     | Starting angle of arc                    |
| `end_angle`        | `int`       | -30     | Ending angle of arc                      |
| `bottom_text_size` | `int`       | 12      | Font size of bottom text (units)         |
| `label_size`       | `int`       | 12      | Font size of label                       |
| `value_size`       | `int`       | 14      | Font size of main value                  |
| `label_spacing`    | `float`     | 0.7     | Spacing of label relative to dial radius |
| `needle`           | `bool`      | `True`  | Show/hide needle                         |
| `odometer`         | `bool`      | `False` | Show odometer style numeric display      |
| `fuel_ticks`       | `bool`      | `False` | Show E and F at start/end points of gauge|

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
    sys.exit(app.exec())
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the issues page
 or submit a pull request.

---

## 🔮 Future Enhancements

⏱️ Real-time updates from sensors or APIs

🌀 Animated needle movement for smooth transitions

🌈 Themes & presets (dark mode, automotive, sci-fi)

📊 Data bindings (connect gauges directly to live values)

🖥️ Demo app with multiple dashboard layouts

## MIT License

Copyright (c) 2025 Joshua Orames

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


