#test_4_servos.py

from esp32_servo_driver import ESP32ServoDriver
import time


servo = ESP32ServoDriver("192.168.4.1")


def move_servo(id_num):
    print(f"\n--- Controlling Servo {id_num} ---")

    if not servo.select_id(id_num):
        print("Failed to select servo")
        return

    print("Moving to middle...")
    servo.middle()
    time.sleep(0.5)

    print("Move +")
    servo.position_plus()
    time.sleep(0.5)

    servo.stop()
    time.sleep(0.3)

    print("Move -")
    servo.position_minus()
    time.sleep(0.5)

    servo.stop()

    info = servo.read_servo_info()
    print("Status:", info)


def main():
    for i in range(1, 5):
        move_servo(i)

    print("\nAll servos tested.")


if __name__ == "__main__":
    main()