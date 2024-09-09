import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)

# Define pins for sensors and LEDs
sensor_pins = {
    'A': 5,  # Herzschrittmacher-Sensor
    'B': 6,  # Knieprothese-Sensor
    'C': 13, # Cochlea-Implantat-Sensor
    'D': 19  # Handprothese-Sensor
}

led_pins = {
    'red': 17,  # LED für richtige Antwort
    'green': 27,
    'yellow': 22,
    'white': 23
}

GPIO.setup(list(sensor_pins.values()), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(list(led_pins.values()), GPIO.OUT)

correct_answer = 'A'

def reset_leds():
    for led in led_pins.values():
        GPIO.output(led, GPIO.LOW)

def light_led(led_color):
    reset_leds()
    GPIO.output(led_pins[led_color], GPIO.HIGH)

def check_answer(channel):
    selected_answer = None

    for key, pin in sensor_pins.items():
        if pin == channel:
            selected_answer = key

    if selected_answer:
        if selected_answer == correct_answer:
            print("Richtig, die richtige Antwort ist Herzschrittmacher.")
            light_led('red')  # Rote LED für richtige Antwort
            time.sleep(5)
        else:
            print("Falsch, die richtige Antwort ist Herzschrittmacher.")
            blink_all_leds()
            time.sleep(3)

def blink_all_leds():
    for _ in range(3):
        for led in led_pins.values():
            GPIO.output(led, GPIO.HIGH)
        time.sleep(0.5)
        reset_leds()
        time.sleep(0.5)

if __name__ == '__main__':
    # Add event detection for each sensor
    for pin in sensor_pins.values():
        GPIO.add_event_detect(pin, GPIO.RISING, callback=check_answer, bouncetime=300)

    try:
        print("Warten auf Benutzereingabe...")
        while True:
            time.sleep(0.1)  # Hauptloop zum Abfragen der Sensoren

    except KeyboardInterrupt:
        print("Beende Programm...")
    finally:
        GPIO.cleanup()
