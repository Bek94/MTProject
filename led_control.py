import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)

# Definieren der LED-Pins
led_pins = {
    'pacemaker': 17,
    'knee': 27,
    'elbow': 22,
    'shoulder': 23
}

GPIO.setup(list(led_pins.values()), GPIO.OUT)

def reset_leds():
    for pin in led_pins.values():
        GPIO.output(pin, GPIO.LOW)

def light_correct_led(implant):
    reset_leds()
    GPIO.output(led_pins[implant], GPIO.HIGH)
    time.sleep(10)
    reset_leds()

def blink_all_leds():
    for _ in range(2):
        for pin in led_pins.values():
            GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.5)
        reset_leds()
        time.sleep(0.5)

if __name__ == '__main__':
    action = sys.argv[1]  # 'correct' oder 'incorrect'
    implant = sys.argv[2] if action == 'correct' else None
    
    reset_leds()
    
    if action == "correct" and implant in led_pins:
        light_correct_led(implant)
    elif action == "incorrect":
        blink_all_leds()

    GPIO.cleanup()
