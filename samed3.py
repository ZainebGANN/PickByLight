import RPi.GPIO as GPIO
import socket
 
# Define the GPIO pins for the LEDs and buttons
LED_PINS = [17, 27, 22, 5, 6, 13, 19, 26]
BUTTON_PINS = [18, 23, 24, 25, 12, 16, 20, 21]  # Define the GPIO pins for the buttons
 
# Predefined materials
PREDEFINED_MATERIALS = ["MATERIAL1", "MATERIAL2", "MATERIAL3", "MATERIAL4"]
 
# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    print(f"Setup LED pin {pin} as OUTPUT")
 
for button_pin in BUTTON_PINS:
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Buttons with internal pull-up resistors
    print(f"Setup button pin {button_pin} as INPUT with pull-up")
 
# Define the server address and port
SERVER_IP = '0.0.0.0'  # Listen on all interfaces
SERVER_PORT = 5000
 
def turn_on_leds():
    for pin in LED_PINS:
        GPIO.output(pin, GPIO.HIGH)
        print(f"LED on pin {pin} turned ON")
 
def turn_off_led(pin):
    GPIO.output(pin, GPIO.LOW)
    print(f"LED on pin {pin} turned OFF")
 
def button_callback(channel):
    led_index = BUTTON_PINS.index(channel)
    turn_off_led(LED_PINS[led_index])
    print(f"Button on pin {channel} pressed, LED on pin {LED_PINS[led_index]} turned OFF")
 
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
    for button_pin in BUTTON_PINS:
        GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=300)
        print(f"Event detection added for button pin {button_pin}")
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
        print("GPIO cleanup done")
 
if __name__ == "__main__":
    main()
