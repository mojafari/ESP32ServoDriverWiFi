# test_matrix.py
from esp32_servo_driver_matrix import MatrixServoDriver
import time

# ESP32 IP
driver = MatrixServoDriver("192.168.4.1", delay=0.4, retries=3)

# Example sequence: column → row for one piece
column_servo = 1
row_servo = 2

driver.activate_column(column_servo)
driver.activate_row(row_servo)

# Next piece
driver.activate_column(3)
driver.activate_row(1)

print("\nMatrix moves completed safely.")