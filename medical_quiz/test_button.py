from gpiozero import Button
import time

buttons = {
    'A': Button(13, pull_up=True, bounce_time=0.1),
    'B': Button(19, pull_up=True, bounce_time=0.1),
    'C': Button(26, pull_up=True, bounce_time=0.1),
    'D': Button(21, pull_up=True, bounce_time=0.1)
}

def create_press_handler(opt):
    def handler():
        print(f"Button {opt} pressed.")
    return handler

def create_release_handler(opt):
    def handler():
        print(f"Button {opt} released.")
    return handler

for option, button in buttons.items():
    button.when_pressed = create_press_handler(option)
    button.when_released = create_release_handler(option)

print("Testing buttons. Press Ctrl+C to exit.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting.")
