# test_driver.py

from esp32_servo_driver import ESP32ServoDriver
import time


def main():
    servo = ESP32ServoDriver("192.168.4.1", timeout=5)

    print("Starting search...")
    servo.start_search()

    time.sleep(2)  # allow search to complete

    print("Servo ID:")
    print(servo.read_servo_id())

    print("Moving to middle...")
    servo.middle()
    time.sleep(0.5)

    print("Increasing speed...")
    servo.speed_plus()

    print("Moving position +...")
    servo.position_plus()
    time.sleep(0.5)

    print("Servo Info:")
    print(servo.read_servo_info())


if __name__ == "__main__":
    main()