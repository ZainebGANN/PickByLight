import RPi.GPIO as GPIO
import socket
import json
import time

# Setup GPIO pins for LEDs and buttons
LED_PINS = [17, 18, 27, 22, 23]  # Replace with actual GPIO pin numbers
BUTTON_PINS = [5, 6, 13, 19, 26]  # Replace with actual GPIO pin numbers

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for led_pin in LED_PINS:
    GPIO.setup(led_pin, GPIO.OUT)
    GPIO.output(led_pin, GPIO.LOW)

for button_pin in BUTTON_PINS:
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Server setup
HOST = '0.0.0.0'
PORT = 5005

def light_up_leds(material_indices):
    # Light up the LEDs corresponding to the material indices
    for i in material_indices:
        GPIO.output(LED_PINS[i], GPIO.HIGH)

def wait_for_button_press():
    while True:
        for i, button_pin in enumerate(BUTTON_PINS):
            if GPIO.input(button_pin) == GPIO.LOW:
                # Turn off the corresponding LED when button is pressed
                GPIO.output(LED_PINS[i], GPIO.LOW)
                return i

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if not data:
                    break

                materials = json.loads(data.decode('utf-8'))
                print(f"Received materials: {materials}")

                # Assuming material_indices correspond to the received materials
                material_indices = list(range(len(materials)))

                # Light up all LEDs at once
                light_up_leds(material_indices)

                for i in material_indices:
                    button_index = wait_for_button_press()
                    conn.sendall(str.encode(materials[button_index]))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
