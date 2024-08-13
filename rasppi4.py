import RPi.GPIO as GPIO
import socket
import json

# GPIO setup
LED_PINS = [17, 27, 22, 10, 9]  # Adjust to your LED pins
BUTTON_PINS = [5, 6, 13, 19, 26]  # Adjust to your button pins
LED_MAP = {'1': LED_PINS[0], '2': LED_PINS[1], '3': LED_PINS[2], '4': LED_PINS[3], '5': LED_PINS[4]}
BUTTON_MAP = {'1': BUTTON_PINS[0], '2': BUTTON_PINS[1], '3': BUTTON_PINS[2], '4': BUTTON_PINS[3], '5': BUTTON_PINS[4]}

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

for pin in BUTTON_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Socket setup
HOST = ''  # Listen on all interfaces
PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

def handle_client(conn):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = json.loads(data.decode())
            action = message.get('action')
            material = message.get('material')
            
            if action == 'light_up' and material in LED_MAP:
                # Light up the corresponding LED
                GPIO.output(LED_MAP[material], GPIO.HIGH)
                # Wait for button press to confirm
                button_pressed = False
                while not button_pressed:
                    for i, pin in enumerate(BUTTON_PINS):
                        if GPIO.input(pin) == GPIO.LOW:
                            # Check if button corresponds to the material
                            if str(i + 1) == material:
                                GPIO.output(LED_MAP[material], GPIO.LOW)
                                button_pressed = True
                                # Send confirmation to Tkinter app
                                confirmation = {'action': 'confirmed', 'material': material}
                                conn.sendall(json.dumps(confirmation).encode())
                                break
            else:
                print(f"Unknown action or material: {action}, {material}")
    finally:
        conn.close()

try:
    while True:
        conn, addr = sock.accept()
        handle_client(conn)
finally:
    GPIO.cleanup()
    sock.close()
