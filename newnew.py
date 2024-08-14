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

def wait_for_confirmation(led_pin, button_pin, material_code):
    GPIO.output(led_pin, GPIO.HIGH)
    while GPIO.input(button_pin):
        pass  # Wait for button press
    GPIO.output(led_pin, GPIO.LOW)
    return material_code

def handle_materials(material_codes):
    active_leds = []
    for material_code in material_codes:
        if material_code in predefined_materials:
            index = predefined_materials.index(material_code)
            led_pin = led_pins[index]
            button_pin = button_pins[index]
            GPIO.output(led_pin, GPIO.HIGH)
            active_leds.append((led_pin, button_pin, material_code))
    
    # Wait for button press and handle each LED
    for led_pin, button_pin, material_code in active_leds:
        confirmed_material = wait_for_confirmation(led_pin, button_pin, material_code)
        send_signal_to_main_app(confirmed_material)

def send_signal_to_main_app(material_code):
    server_ip = "10.110.20.205"  # Replace with your Raspberry Pi IP address
    server_port = 6000  # Different port for sending back the signal
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    client_socket.sendall(material_code.encode())
    client_socket.close()

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
        material_codes = client_socket.recv(1024).decode().split(',')
        print("Received material codes:", material_codes)
        handle_materials(material_codes)
        client_socket.close()

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        GPIO.cleanup()
