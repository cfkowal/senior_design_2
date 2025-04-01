import lgpio

class LimitSwitch:
    def __init__(self, gpio_pin, chip=0, active_low=True):
        """
        Represents a digital limit switch using lgpio.
        :param gpio_pin: GPIO pin number (BCM)
        :param chip: GPIO chip (default 0 for /dev/gpiochip0)
        :param active_low: True if pressed = logic low (normally closed switch)
        """
        self.gpio_pin = gpio_pin
        self.active_low = active_low
        self.handle = lgpio.gpiochip_open(chip)
        lgpio.gpio_claim_input(self.handle, gpio_pin)

    def is_triggered(self):
        """Return True if the switch is currently triggered"""
        value = lgpio.gpio_read(self.handle, self.gpio_pin)
        return (value == 0) if self.active_low else (value == 1)

    def close(self):
        """Release the GPIO handle"""
        lgpio.gpiochip_close(self.handle)
