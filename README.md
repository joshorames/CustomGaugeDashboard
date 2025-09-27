# 🚗 CustomGauge Dashboard (PySide6)

<img width="1234" height="459" alt="image" src="https://github.com/user-attachments/assets/e03f0d74-01f7-4874-8d26-8c1751ac4b28" />
<img width="1461" height="904" alt="image" src="https://github.com/user-attachments/assets/b4584aab-d0e1-4f26-b3c2-3278e591f1e0" />

**CustomGauge** is a fully customizable PySide6 widget for building beautiful dashboards with gauges — perfect for automotive-style UIs, monitoring panels, or any real-time visualization of values.

---
## Create Reusable Pi Image
🔹 1. Prepare a “master” Raspberry Pi

Flash a fresh Raspberry Pi OS onto an SD card.

Boot the Pi and set it up (update packages, set hostname, Wi-Fi, etc. if you like).

sudo apt update && sudo apt upgrade -y


Install Python + dependencies for your project:

sudo apt install python3 python3-pip git -y


Clone your repo and install requirements:

cd ~
git clone https://github.com/joshorames/CustomGaugeDashboard.git
cd CustomGaugeDashboard
pip3 install -r requirements.txt


Configure autostart for GUI (as I explained earlier with ~/.config/autostart/dashboard.desktop).

Reboot and test: your dashboard should pop up on boot.

🔹 2. Clean up before making the image

To keep the image small:

sudo apt autoremove -y
sudo apt clean


(Optional: delete history/logs if you want a “fresh” feel.)

history -c
sudo rm -rf /var/log/*

🔹 3. Shut down the Pi
sudo poweroff


Remove the SD card and plug it into another computer (Linux or Windows with tools).

🔹 4. Create a custom image
On Linux/macOS

Find the SD card device:

lsblk


Then clone it into an image file (replace sdX with your SD card device):

sudo dd if=/dev/sdX of=~/CustomGaugeDashboard.img bs=4M status=progress
sync


Now CustomGaugeDashboard.img is your custom OS image.

On Windows

Use Win32 Disk Imager:

Insert SD card.

Open Win32 Disk Imager.

Choose an output file name (e.g. CustomGaugeDashboard.img).

Select the SD card drive.

Click Read (this copies SD → image).

🔹 5. Compress & distribute (optional)

Compress the image so it’s smaller:

xz -z -9 CustomGaugeDashboard.img


Now you can share CustomGaugeDashboard.img.xz.

🔹 6. Flash to other Pis

Use Raspberry Pi Imager, balenaEtcher, or dd again to write the image back to SD cards. Any Pi you boot with it will:

Auto-login

Launch your dashboard GUI on boot
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

## License

Copyright (c) 2025 Josh Orames

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to use,
copy, modify, and distribute the Software for personal, educational, or
research purposes only, subject to the following conditions:

- Commercial use of the Software is strictly prohibited without prior written
  permission from the copyright holder.
- The copyright holder (Josh Orames) reserves all rights to commercial use,
  including but not limited to licensing, distribution, and derivative works.
- The above copyright notice and this permission notice shall be included
  in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.


