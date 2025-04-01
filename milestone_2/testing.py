import lgpio
import time

chip = 0
pin = 3  # your GPIO pin
handle = lgpio.gpiochip_open(chip)

# Explicitly claim input with pull-up
lgpio.gpio_claim_input(handle, pin, lgpio.SET_PULL_UP)

try:
    while True:
        val = lgpio.gpio_read(handle, pin)
        print("GPIO", pin, "reads:", val)
        time.sleep(0.1)
except KeyboardInterrupt:
    lgpio.gpiochip_close(handle)
