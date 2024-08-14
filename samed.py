import RPi.GPIO as GPIO
import socket
 
# Define the GPIO pins for the LEDs and buttons
LED_PINS = [17, 27, 22, 5, 6, 13, 19, 26]
BUTTON_PINS = [18, 23, 24, 25, 12, 16, 20, 21]  # Define the GPIO pins for the buttons
 
# Predefined materials
PREDEFINED_MATERIALS = ["MATERIAL1", "MATERIAL2", "MATERIAL3", "MATERIAL4", "MATERIAL5", "MATERIAL6", "MATERIAL7", "MATERIAL8"]
 
# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
 
for pin in BUTTON_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button with internal pull-up resistor
 
# Define the server address and port
SERVER_IP = '0.0.0.0'  # Listen on all interfaces
SERVER_PORT = 5000
 
def turn_on_leds():
    for pin in LED_PINS:
        GPIO.output(pin, GPIO.HIGH)
 
def turn_off_led(pin):
    GPIO.output(pin, GPIO.LOW)
 
def button_callback(channel):
    button_index = BUTTON_PINS.index(channel)
    led_pin = LED_PINS[button_index]
    turn_off_led(led_pin)
 
def handle_client_connection(client_socket):
    try:
        request = client_socket.recv(1024).decode()
        print(f"Received: {request}")
        if request.startswith('Material:'):
            material_code = request.split(':')[1].strip()
            print(f"Material code received: {material_code}")
            if material_code in PREDEFINED_MATERIALS:
                index = PREDEFINED_MATERIALS.index(material_code)
                GPIO.output(LED_PINS[index], GPIO.HIGH)  # Turn on the corresponding LED
                client_socket.sendall(b'LED turned on for material code\n')
            else:
                client_socket.sendall(b'Material code not recognized\n')
        else:
            client_socket.sendall(b'Unknown command\n')
    except Exception as e:
        print(f"Error handling client connection: {e}")
    finally:
        client_socket.close()
 
def main():
    for pin in BUTTON_PINS:
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_callback, bouncetime=300)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(5)
    print(f"Listening on {SERVER_IP}:{SERVER_PORT}")
 
    try:
        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")
            handle_client_connection(client_socket)
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server.close()
        GPIO.cleanup()
 
if __name__ == "__main__":
    main()
