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

# Predefined materials for each LED and button
PREDEFINED_MATERIALS = [
    'Material_A',  # Corresponds to LED 0 and Button 0
    'Material_B',  # Corresponds to LED 1 and Button 1
    'Material_C',  # Corresponds to LED 2 and Button 2
    'Material_D',  # Corresponds to LED 3 and Button 3
    'Material_E',  # Corresponds to LED 4 and Button 4
]

# Server setup
HOST = '0.0.0.0'
PORT = 5005

def light_up_leds(material_indices):
    for i in material_indices:
        if i < len(LED_PINS):  # Ensure the index is within bounds
            GPIO.output(LED_PINS[i], GPIO.HIGH)
        else:
            print(f"Invalid LED index: {i}")

def wait_for_button_press():
    while True:
        for i, button_pin in enumerate(BUTTON_PINS):
            if GPIO.input(button_pin) == GPIO.LOW:
                # Turn off the corresponding LED when button is pressed
                GPIO.output(LED_PINS[i], GPIO.LOW)
                print(f"Button {i} pressed")
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

                received_data = json.loads(data.decode('utf-8'))
                print(f"Received data: {received_data}")

                # Use predefined materials for button indices
                material_indices = [PREDEFINED_MATERIALS.index(mat) for mat in received_data if mat in PREDEFINED_MATERIALS]
                print(f"Material indices: {material_indices}")

                light_up_leds(material_indices)

                for _ in material_indices:
                    button_index = wait_for_button_press()
                    print(f"Button index: {button_index}")

                    if 0 <= button_index < len(PREDEFINED_MATERIALS):
                        material = PREDEFINED_MATERIALS[button_index]
                        conn.sendall(str.encode(material))
                    else:
                        print(f"Button index out of range: {button_index}")
                        conn.sendall(str.encode("Error: Button index out of range"))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
