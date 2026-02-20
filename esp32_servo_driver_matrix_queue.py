# esp32_servo_driver_matrix_queue.py
import time
from collections import deque
from esp32_servo_driver import ESP32ServoDriver

class MatrixServoDriver:
    def __init__(self, ip_address, delay=0.3, retries=3):
        """
        ip_address : str : ESP32 IP, e.g., '192.168.4.1'
        delay      : float : delay between commands to avoid disconnects
        retries    : int   : number of retries if a command fails
        """
        self.driver = ESP32ServoDriver(ip_address)
        self.delay = delay
        self.retries = retries
        self.queue = deque()

    def _safe_command(self, servo_id, command, *args):
        """Select servo, execute command safely with retries."""
        for attempt in range(self.retries):
            if not self.driver.select_id(servo_id):
                print(f"[WARN] Failed to select servo {servo_id}, attempt {attempt+1}")
                time.sleep(self.delay)
                continue
            try:
                getattr(self.driver, command)(*args)
                time.sleep(self.delay)
                return True
            except Exception as e:
                print(f"[WARN] Command '{command}' failed for servo {servo_id}: {e}")
                time.sleep(self.delay)
        print(f"[ERROR] Command '{command}' failed for servo {servo_id} after {self.retries} retries")
        return False

    def enqueue_piece(self, column_servo, row_servo):
        """
        Add a piece to the processing queue. Each piece is a (column, row) tuple.
        """
        self.queue.append((column_servo, row_servo))

    def _process_servo(self, servo_id, servo_type="generic"):
        """
        Execute a single servo move: middle → plus → minus
        """
        print(f"\nActivating {servo_type} servo {servo_id}...")
        self._safe_command(servo_id, "middle")
        self._safe_command(servo_id, "position_plus")
        self._safe_command(servo_id, "position_minus")
        status = self.driver.read_servo_info()
        print(f"{servo_type.capitalize()} servo {servo_id} status: {status}")

    def process_queue(self):
        """
        Execute all queued pieces sequentially: column then row for each piece
        """
        print("\nProcessing queue...")
        while self.queue:
            column_servo, row_servo = self.queue.popleft()
            self._process_servo(column_servo, "column")
            self._process_servo(row_servo, "row")
        print("\nAll queued pieces processed.")