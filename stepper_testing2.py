import lgpio
import time

# BCM GPIOs
NORTH_DIR_PIN = 11
NORTH_STEP_PIN = 12
SOUTH_DIR_PIN = 9
SOUTH_STEP_PIN = 13
# Open a GPIO handle (chip 0 is default for main Pi GPIOs)
h = lgpio.gpiochip_open(0)

# Set pin modes
lgpio.gpio_claim_output(h, NORTH_DIR_PIN, 0)
lgpio.gpio_claim_output(h, NORTH_STEP_PIN, 0)
lgpio.gpio_claim_output(h, SOUTH_DIR_PIN, 0)
lgpio.gpio_claim_output(h, SOUTH_STEP_PIN, 0)

# Set direction (1 or 0)
lgpio.gpio_write(h, SOUTH_DIR_PIN, 0)
lgpio.gpio_write(h, NORTH_DIR_PIN, 1)


# PWM-style control
frequency = 1000  # Hz
duty_cycle = 50   # percent
duration = 0.75    # seconds

period = 1.0 / frequency
high_time = period * (duty_cycle / 100.0)
low_time = period - high_time
steps = int(duration * frequency)

try:
    print("Running stepper...")
    for _ in range(steps):
        lgpio.gpio_write(h, NORTH_STEP_PIN, 1)
        lgpio.gpio_write(h, SOUTH_STEP_PIN, 1)
        time.sleep(high_time)
        lgpio.gpio_write(h, NORTH_STEP_PIN, 0)
        lgpio.gpio_write(h, SOUTH_STEP_PIN, 0)
        time.sleep(low_time)
        
    lgpio.gpio_write(h, SOUTH_DIR_PIN, 1)
    lgpio.gpio_write(h, NORTH_DIR_PIN, 0)
    
    for _ in range(steps):
        lgpio.gpio_write(h, NORTH_STEP_PIN, 1)
        lgpio.gpio_write(h, SOUTH_STEP_PIN, 1)
        time.sleep(high_time)
        lgpio.gpio_write(h, NORTH_STEP_PIN, 0)
        lgpio.gpio_write(h, SOUTH_STEP_PIN, 0)
        time.sleep(low_time)

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    # Release GPIOs and close the chip
    lgpio.gpiochip_close(h)
    print("GPIO released.")
