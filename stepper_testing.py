import Jetson.GPIO as GPIO
import time


STEP_PIN = 18
DIR_PIN = 22
EN_PIN = 24

def setup_stepper():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(STEP_PIN, GPIO.OUT)
    GPIO.setup(DIR_PIN, GPIO.OUT)
    GPIO.setup(EN_PIN, GPIO.OUT)

    GPIO.output(EN_PIN, GPIO.HIGH)

def move_stepper(steps, direction, speed=0.0001):
    """
    true for clockwise, false for ccw
    """
    if direction:
        GPIO.output(DIR_PIN, GPIO.LOW)
    else:
        GPIO.output(DIR_PIN, GPIO.HIGH) # THIS IS OUTPUTTING 1 VOLT

    GPIO.output(EN_PIN, GPIO.LOW)

    for _ in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(speed)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(speed)

def cleanup():
    GPIO.cleanup()


if __name__ == "__main__":
    try:
        setup_stepper()
        while(1):
            print("Running...")
            move_stepper(5000, True)
            time.sleep(1)
            move_stepper(5000, False)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\Program Stopped By User")
    finally:
        cleanup()
            