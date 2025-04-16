# io_controller.py

import lgpio
import time

class PlotterIO:
    def __init__(self, chip, start_button, error_led, solving_led, writing_led, debounce_ms=50):
        self.handle = lgpio.gpiochip_open(chip)

        self.start_button = start_button
        self.led_pins = {
            "error": error_led,
            "solving": solving_led,
            "writing": writing_led
        }

        self.debounce_ms = debounce_ms / 1000.0  # convert to seconds

        # Input button
        lgpio.gpio_claim_input(self.handle, self.start_button)

        # LEDs (active high)
        for pin in self.led_pins.values():
            lgpio.gpio_claim_output(self.handle, pin, 0)  

    def is_start_pressed(self):
        return lgpio.gpio_read(self.handle, self.start_button) == 1

    def wait_for_press(self):
        """Wait for a clean press-and-release cycle, debounced and foolproof."""
        print("Waiting for start button...")

        while True:
            if self.is_start_pressed():
                press_time = time.time()
                while self.is_start_pressed():
                    time.sleep(0.01)
                release_time = time.time()

                if (release_time - press_time) >= self.debounce_ms:
                    print("Button press detected")
                    return
                else:
                    print("Ignored bounce/false press")

            time.sleep(0.01)

    def set_led(self, name, state):
        """Set LED state: true is on, false is off, active high"""
        if name in self.led_pins:
            lgpio.gpio_write(self.handle, self.led_pins[name], 1 if state else 0)
    
    def blink(self, name):
            if name in self.led_pins:
                for _ in range(15):
                    self.set_led(name, True)
                    time.sleep(0.2)
                    self.set_led(name, False)
                    time.sleep(0.2)
            
                self.set_led(name, False)
    
    def all_off(self):
        """Turn off all LEDs"""
        for pin in self.led_pins.values():
            lgpio.gpio_write(self.handle, pin, 0)

    def close(self):
        self.all_off()
        lgpio.gpiochip_close(self.handle)
