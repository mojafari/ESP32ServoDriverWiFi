# test_matrix_queue.py
from esp32_servo_driver_matrix_queue import MatrixServoDriver

driver = MatrixServoDriver("192.168.4.1", delay=0.4, retries=3)

# Enqueue pieces as (column_servo_id, row_servo_id)
driver.enqueue_piece(1, 2)
driver.enqueue_piece(3, 1)
driver.enqueue_piece(4, 2)
driver.enqueue_piece(2, 3)

# Process queue sequentially, safely
driver.process_queue()