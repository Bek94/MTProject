import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led_pins = {
    'red': 17,
    'green': 27,
    'yellow': 22,
    'white': 23
}

GPIO.setup(list(led_pins.values()), GPIO.OUT)

def light_correct_answer():
    GPIO.output(led_pins['red'], GPIO.HIGH)
    time.sleep(10)
    GPIO.output(led_pins['red'], GPIO.LOW)

def blink_all_leds():
    for _ in range(3):
        for pin in led_pins.values():
            GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.5)
        reset_leds()
        time.sleep(0.5)

def reset_leds():
    for pin in led_pins.values():
        GPIO.output(pin, GPIO.LOW)

if __name__ == '__main__':
    light_correct_answer()  # Demo für die richtige Antwort
    blink_all_leds()        # Demo für falsche Antworten

    GPIO.cleanup()
