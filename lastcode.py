import RPi.GPIO as GPIO
import time
import socket

# Setup GPIO mode and pins
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the LEDs and the button
LED_PINS = [18, 24, 25, 12, 16]  # GPIO pins for the LEDs
BUTTON_PINS = [23, 22, 27, 5, 6]  # GPIO pins for the buttons

# Setup GPIO pins
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Ensure all LEDs are initially off

for pin in BUTTON_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Predefined material codes
PREDEFINED_MATERIALS = ["3MC10XYZ", "3MC20ABC", "3MC30DEF", "3MC40GHI", "3MC50JKL"]

def light_up_leds_and_wait_for_confirmation(matched_materials):
    for i, material in enumerate(matched_materials):
        if material in PREDEFINED_MATERIALS:
            GPIO.output(LED_PINS[i], GPIO.HIGH)  # Turn on the corresponding LED
    print("All LEDs are ON. Waiting for button presses...")

    while matched_materials:
        for i, pin in enumerate(BUTTON_PINS):
            if GPIO.input(pin) == GPIO.LOW:  # Button pressed
                print(f"Button {i+1} pressed. Turning off LED.")
                GPIO.output(LED_PINS[i], GPIO.LOW)  # Turn off the corresponding LED
                matched_materials.pop(0)  # Remove the material from the list
                break
        time.sleep(0.1)  # Debounce delay

try:
    # Main loop
    while True:
        # For this example, replace this with actual material fetching logic
        matched_materials = []
        for i in range(5):
            matched_material = input(f"Enter the matched material code {i+1}: ")
            matched_materials.append(matched_material)

        # Call the function to light up the LEDs and wait for button confirmation
        light_up_leds_and_wait_for_confirmation(matched_materials)

except KeyboardInterrupt:
    print("Program interrupted. Cleaning up GPIO...")

finally:
    GPIO.cleanup()  # Clean up all the GPIO pins
