import RPi.GPIO as GPIO
import time
import sys
import subprocess

# GPIO Setup
GPIO.setmode(GPIO.BCM)

# Definieren der LED- und Sensor-Pins
led_pins = {
    'pacemaker': 17,
    'knee': 27,
    'elbow': 22,
    'shoulder': 23
}

sensor_pins = {
    'pacemaker': 5,
    'knee': 6,
    'elbow': 13,
    'shoulder': 19
}

GPIO.setup(list(led_pins.values()), GPIO.OUT)
GPIO.setup(list(sensor_pins.values()), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Funktion zum Zurücksetzen der LEDs
def reset_leds():
    for pin in led_pins.values():
        GPIO.output(pin, GPIO.LOW)

# Funktion zum Aktivieren einer korrekten LED
def light_correct_led(implant):
    reset_leds()
    GPIO.output(led_pins[implant], GPIO.HIGH)
    time.sleep(10)
    reset_leds()

# Funktion zum Blinken aller LEDs bei falscher Antwort
def blink_all_leds():
    for _ in range(2):
        for pin in led_pins.values():
            GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.5)
        reset_leds()
        time.sleep(0.5)

# Überwache Sensoren für den "Mehrinformationsmodus"
def check_sensor_input():
    while True:
        for implant, pin in sensor_pins.items():
            if GPIO.input(pin) == GPIO.HIGH:
                # Sensor-Interaktion erkannt, sende das Implantat an die GUI
                print(implant)
                time.sleep(1)  # Verhindert Mehrfachauslösungen
        time.sleep(0.1)

if __name__ == '__main__':
    try:
        mode = sys.argv[1]  # 'quiz' oder 'info'
        
        if mode == 'quiz':
            result = sys.argv[2]  # 'correct' oder 'incorrect'
            implant = sys.argv[3] if result == 'correct' else None
            
            if result == "correct" and implant in led_pins:
                light_correct_led(implant)
            elif result == "incorrect":
                blink_all_leds()
        elif mode == 'info':
            check_sensor_input()

    except KeyboardInterrupt:
        print("Programm beendet.")
    finally:
        GPIO.cleanup()
