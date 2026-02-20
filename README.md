# ESP32 Servo Driver & Matrix Control

This repository contains Python drivers and example scripts to control **MY-series ESP32 servo drivers** over WiFi. It supports single servo control, multi-servo sequences, and matrix-style control for projects such as conveyor sorting or robotics grids.  

---

## 📦 Files Included

### Drivers
| File | Description |
|------|-------------|
| `esp32_servo_driver.py` | Core HTTP driver for controlling a single ESP32-connected servo. Supports commands, status read, retries, and parsing. |
| `esp32_servo_driver_matrix.py` | Matrix servo driver: safely activates column and row servos sequentially. |
| `esp32_servo_driver_matrix_queue.py` | Matrix servo driver with a queue system for multiple pieces. Executes column → row moves safely in order. |

### Test / Example Scripts
| File | Description |
|------|-------------|
| `test_driver.py` | Basic test of a single servo: search, move, read status. |
| `test_4_servos.py` | Sequentially moves 4 servos connected to the ESP32. |
| `test_4_servos_parallel.py` | Round-robin style move sequence for 4 servos to simulate faster multi-servo operations. |
| `test_matrix.py` | Example of activating column and row servos using `esp32_servo_driver_matrix.py`. |
| `test_matrix_queue.py` | Example of enqueuing multiple pieces and processing them sequentially with safe servo commands. |

---

## ⚡ Prerequisites

- Python 3.8+  
- `requests` library (`pip install requests`)  
- ESP32 running the compatible MY-series servo firmware  
- ESP32 IP address on the local WiFi network (default example: `192.168.4.1`)  

---

## 🚀 Getting Started

### 1. Single Servo Example

```python
from esp32_servo_driver import ESP32ServoDriver
import time

servo = ESP32ServoDriver("192.168.4.1")

# Move Servo 1
servo.select_id(1)
servo.middle()
servo.position_plus()
servo.position_minus()
info = servo.read_servo_info()
print(info)
