import RPi.GPIO as GPIO
import socket

# Define GPIO pin numbers for LEDs and buttons
led_pins = [18, 23, 24, 25, 12]  # Replace with your GPIO pins
button_pins = [5, 6, 13, 19, 26]  # Replace with your GPIO pins

# Predefined materials and corresponding LED indices
predefined_materials = ["3MC0200070519", "3MC1098060001", "3MC0245050300", "Material4", "Material5"]

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def wait_for_all_confirmations():
    # Light up all LEDs
    for pin in led_pins:
        GPIO.output(pin, GPIO.HIGH)
    
    # Wait for confirmation from all buttons
    confirmed_buttons = set()
    while len(confirmed_buttons) < len(button_pins):
        for i, button_pin in enumerate(button_pins):
            if GPIO.input(button_pin) == GPIO.LOW and i not in confirmed_buttons:
                confirmed_buttons.add(i)
                GPIO.output(led_pins[i], GPIO.LOW)  # Turn off LED when the corresponding button is pressed

def handle_material(material_code):
    if material_code in predefined_materials:
        print(f"Handling material: {material_code}")
        wait_for_all_confirmations()

def start_server():
    server_ip = "10.110.20.205"  # Replace with your Raspberry Pi IP address
    server_port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print("Server listening on {}:{}".format(server_ip, server_port))

    while True:
        client_socket, addr = server_socket.accept()
        print("Connection from:", addr)
        material_code = client_socket.recv(1024).decode()
        print("Received material code:", material_code)
        handle_material(material_code)
        client_socket.close()

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        GPIO.cleanup()
