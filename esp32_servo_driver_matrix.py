# esp32_servo_driver_matrix.py
import time
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

    def _safe_command(self, servo_id, command, *args):
        """
        Select servo, execute a driver command, retry if fails.
        """
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

    def activate_column(self, servo_id):
        """
        Move a column servo: middle → position plus → position minus
        """
        print(f"\nActivating column servo {servo_id}...")
        self._safe_command(servo_id, "middle")
        self._safe_command(servo_id, "position_plus")
        self._safe_command(servo_id, "position_minus")
        status = self.driver.read_servo_info()
        print(f"Column servo {servo_id} status: {status}")

    def activate_row(self, servo_id):
        """
        Move a row servo: middle → position plus → position minus
        """
        print(f"\nActivating row servo {servo_id}...")
        self._safe_command(servo_id, "middle")
        self._safe_command(servo_id, "position_plus")
        self._safe_command(servo_id, "position_minus")
        status = self.driver.read_servo_info()
        print(f"Row servo {servo_id} status: {status}")