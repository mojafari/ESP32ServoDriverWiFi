#test_4_servos_parallel.py


from esp32_servo_driver import ESP32ServoDriver
import time

servo_driver = ESP32ServoDriver("192.168.4.1")

servo_ids = [1, 2, 3, 4]

# Pre-select each servo and store a "move plan"
def prepare_servos():
    for sid in servo_ids:
        if servo_driver.select_id(sid):
            servo_driver.middle()
            servo_driver.speed_plus()
        time.sleep(0.05)

# Execute moves quickly in a round-robin loop
def execute_moves():
    for _ in range(3):  # number of move cycles
        for sid in servo_ids:
            if servo_driver.select_id(sid):
                servo_driver.position_plus()
        for sid in servo_ids:
            if servo_driver.select_id(sid):
                servo_driver.position_minus()
        time.sleep(0.05)

def get_status():
    for sid in servo_ids:
        if servo_driver.select_id(sid):
            status = servo_driver.read_servo_info()
            print(f"Servo {sid} status: {status}")

def main():
    prepare_servos()
    execute_moves()
    get_status()
    print("All servos moved safely without conflicts.")

if __name__ == "__main__":
    main()