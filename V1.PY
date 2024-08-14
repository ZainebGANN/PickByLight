import RPi.GPIO as GPIO
import socket
import threading
 
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
 
def wait_for_confirmation(button_pin, led_pin, event):
    GPIO.output(led_pin, GPIO.HIGH)
    while GPIO.input(button_pin):
        pass  # Wait for button press
    GPIO.output(led_pin, GPIO.LOW)
    event.set()
 
def handle_material(material_code):
    leds_to_light = []
    events = []
    threads = []
    for i, code in enumerate(predefined_materials):
        if material_code == code:
            leds_to_light.append((led_pins[i], button_pins[i]))
    # Create threads for each LED/button pair
    for led_pin, button_pin in leds_to_light:
        event = threading.Event()
        thread = threading.Thread(target=wait_for_confirmation, args=(button_pin, led_pin, event))
        threads.append(thread)
        events.append(event)
    # Start all threads
    for thread in threads:
        thread.start()
    # Wait for all events to be set (all button presses confirmed)
    for event in events:
        event.wait()
 
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
