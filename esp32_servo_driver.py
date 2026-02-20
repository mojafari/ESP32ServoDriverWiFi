# esp32_servo_driver.py

import requests
import time


class ESP32ServoDriver:
    def __init__(self, ip, timeout=2, retries=3, retry_delay=0.2):
        """
        ESP32 Servo Driver over HTTP

        :param ip: IP address of the ESP32
        :param timeout: HTTP request timeout (seconds)
        :param retries: number of retries for read endpoints
        :param retry_delay: delay between retries (seconds)
        """
        self.base_url = f"http://{ip}"
        self.timeout = timeout
        self.retries = retries
        self.retry_delay = retry_delay

    # =========================================================
    # Internal HTTP methods
    # =========================================================

    def _fire_and_forget(self, endpoint, params=None):
        """Send /cmd requests without expecting response (ESP32 may close connection early)."""
        try:
            requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                timeout=self.timeout,
                stream=True
            )
        except requests.exceptions.RequestException:
            # Ignore connection closed errors for commands
            pass
        return True

    def _get_with_retry(self, endpoint):
        """GET request with retry logic for read endpoints."""
        url = f"{self.base_url}/{endpoint}"
        for _ in range(self.retries):
            try:
                r = requests.get(url, timeout=self.timeout)
                return r.text
            except requests.exceptions.RequestException:
                time.sleep(self.retry_delay)
        print(f"[ERROR] Failed after {self.retries} retries → {endpoint}")
        return None

    # =========================================================
    # Core command interface
    # =========================================================

    def send_cmd(self, inputT, inputI, inputA=0, inputB=0):
        params = {"inputT": inputT, "inputI": inputI, "inputA": inputA, "inputB": inputB}
        return self._fire_and_forget("cmd", params)

    # =========================================================
    # Read interface
    # =========================================================

    def read_servo_info_raw(self):
        """Return raw /readSTS response."""
        return self._get_with_retry("readSTS")

    def read_servo_id(self):
        """Return raw /readID response."""
        return self._get_with_retry("readID")

    # =========================================================
    # Clean Servo Info Parser
    # =========================================================

    def read_servo_info(self):
        """Return servo info as a clean dictionary with numbers converted."""
        raw = self.read_servo_info_raw()
        if not raw:
            return None

        # Replace <p> with newline
        clean = raw.replace("<p>", "\n")
        lines = clean.split("\n")

        data = {}

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Split multiple key:value pairs per line (separated by double space)
            parts = line.split("  ")
            for part in parts:
                if ":" not in part:
                    continue
                key, value = part.split(":", 1)
                key = key.strip()
                value = value.strip()

                # Convert numeric values
                try:
                    if "." in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    pass  # keep as string if not numeric

                data[key] = value

        return data

    # =========================================================
    # Servo ID Selection
    # =========================================================

    def select_id(self, target_id):
        """Switch active servo ID safely."""
        try:
            target_id = int(target_id)
        except ValueError:
            print("Invalid target ID")
            return False

        current_info = self.read_servo_info()
        if not current_info:
            return False

        try:
            current_id = int(current_info.get("Active ID"))
        except (TypeError, ValueError):
            print("Invalid Active ID")
            return False

        # Loop until target ID is active
        while current_id != target_id:
            if current_id < target_id:
                self.send_cmd(0, 1)  # ID+
            else:
                self.send_cmd(0, -1)  # ID-

            time.sleep(0.15)

            current_info = self.read_servo_info()
            if not current_info:
                return False

            try:
                current_id = int(current_info.get("Active ID"))
            except (TypeError, ValueError):
                return False

        return True

    # =========================================================
    # Motion / UI button equivalents
    # =========================================================

    def start_search(self): return self.send_cmd(9, 0)
    def id_select_plus(self): return self.send_cmd(0, 1)
    def id_select_minus(self): return self.send_cmd(0, -1)

    def middle(self): return self.send_cmd(1, 1)
    def stop(self): return self.send_cmd(1, 2)
    def release(self): return self.send_cmd(1, 3)
    def torque(self): return self.send_cmd(1, 4)

    def position_plus(self): return self.send_cmd(1, 5)
    def position_minus(self): return self.send_cmd(1, 6)

    def speed_plus(self): return self.send_cmd(1, 7)
    def speed_minus(self): return self.send_cmd(1, 8)

    def set_middle_position(self): return self.send_cmd(1, 11)
    def set_servo_mode(self): return self.send_cmd(1, 12)
    def set_motor_mode(self): return self.send_cmd(1, 13)

    def start_serial_forwarding(self): return self.send_cmd(1, 14)
    def stop_serial_forwarding(self): return self.send_cmd(1, 15)

    def set_new_id(self): return self.send_cmd(1, 16)

    def set_role_normal(self): return self.send_cmd(1, 17)
    def set_role_leader(self): return self.send_cmd(1, 18)
    def set_role_follower(self): return self.send_cmd(1, 19)

    def rainbow_on(self): return self.send_cmd(1, 20)
    def rainbow_off(self): return self.send_cmd(1, 21)

    # =========================================================
    # Utility
    # =========================================================

    def wait(self, seconds):
        time.sleep(seconds)