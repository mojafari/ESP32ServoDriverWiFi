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
```

---

### 2. Sequential Multi-Servo Example

```python
from esp32_servo_driver import ESP32ServoDriver
import time

servo = ESP32ServoDriver("192.168.4.1")

for servo_id in [1, 2, 3, 4]:
    if servo.select_id(servo_id):
        servo.middle()
        servo.position_plus()
        servo.position_minus()
        print(f"Servo {servo_id} status:", servo.read_servo_info())
```

---

### 3. Matrix Control (Column → Row)

```python
from esp32_servo_driver_matrix import MatrixServoDriver

driver = MatrixServoDriver("192.168.4.1")

# Activate a column servo then a row servo
driver.activate_column(1)
driver.activate_row(2)

driver.activate_column(3)
driver.activate_row(1)
```

---

### 4. Matrix Queue Control (Multiple Pieces)

```python
from esp32_servo_driver_matrix_queue import MatrixServoDriver

driver = MatrixServoDriver("192.168.4.1")

# Queue pieces: (column_servo_id, row_servo_id)
driver.enqueue_piece(1, 2)
driver.enqueue_piece(3, 1)
driver.enqueue_piece(4, 2)
driver.enqueue_piece(2, 3)

# Execute queued moves sequentially
driver.process_queue()
```

---

## 🔧 Notes / Tips

- The ESP32 may occasionally **close connections** during rapid sequences. Drivers implement retry logic to handle this.  
- Use `delay` in matrix drivers to avoid disconnects (`0.3–0.5s` recommended).  
- Column and row servos should **not move simultaneously** on the same ESP32 instance; use sequential activation for reliability.  
- To debug: monitor ESP32 **serial output** or **WiFi connection** for errors.  
- `activate_column()` and `activate_row()` are identical in behavior but used for readability in matrix projects.  

---

## 🧰 Recommended Workflow for Students

1. Test **single servo** using `test_driver.py`  
2. Test **all 4 servos sequentially** with `test_4_servos.py`  
3. Experiment with **parallel moves** using `test_4_servos_parallel.py` (round-robin style)  
4. Implement **matrix sorting** using `test_matrix.py`  
5. Process **multiple queued pieces safely** using `test_matrix_queue.py`  

---


### 📖 References

- **ESP32 Servo Driver Expansion Board (Waveshare)** — https://www.waveshare.com/product/servo-driver-with-esp32.htm  
- **ST3215 Series Smart Servo (Waveshare)** — https://www/waveshare.com/product/st3215-servo.htm  
- **ESP32 HTTP API (Unofficial)** — `/cmd`, `/readSTS`, `/readID` endpoints provided by the onboard firmware.  
- **ESP‑NOW (ESP32 Peer‑to‑Peer Protocol)** — https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api/protocols/esp_now.html  
- **ESP32 WiFi / Web Server (Arduino framework)** — official docs for networking and web servers.
