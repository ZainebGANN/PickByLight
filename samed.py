[13:34] Fkiri, Samed
import RPi.GPIO as GPIO

import socket
 
# Define the GPIO pins for the LEDs and buttons

LED_PINS = [17, 27, 22, 5, 6, 13, 19, 26]

BUTTON_PIN = 23  # Define the GPIO pin for the button
 
# Predefined materials

PREDEFINED_MATERIALS = ["MATERIAL1", "MATERIAL2", "MATERIAL3", "MATERIAL4"]
 
# Setup GPIO

GPIO.setmode(GPIO.BCM)

for pin in LED_PINS:

    GPIO.setup(pin, GPIO.OUT)

    GPIO.output(pin, GPIO.LOW)
 
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button with internal pull-up resistor
 
# Define the server address and port

SERVER_IP = '0.0.0.0'  # Listen on all interfaces

SERVER_PORT = 5000
 
def turn_on_leds():

    for pin in LED_PINS:

        GPIO.output(pin, GPIO.HIGH)
 
def turn_off_leds():

    for pin in LED_PINS:

        GPIO.output(pin, GPIO.LOW)
 
def button_callback(channel):

    turn_off_leds()
 
def handle_client_connection(client_socket):

    try:

        request = client_socket.recv(1024).decode()

        print(f"Received: {request}")

        if request.startswith('Material:'):

            material_code = request.split(':')[1].strip()

            print(f"Material code received: {material_code}")

            if material_code in PREDEFINED_MATERIALS:

                turn_on_leds()  # Turn on LEDs for the material code

                client_socket.sendall(b'LEDs turned on for material code\n')

            else:

                client_socket.sendall(b'Material code not recognized\n')

        else:

            client_socket.sendall(b'Unknown command\n')

    except Exception as e:

        print(f"Error handling client connection: {e}")

    finally:

        client_socket.close()
 
def main():

    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

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

 
