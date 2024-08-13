import RPi.GPIO as GPIO
import time

# Setup GPIO mode and pins
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the LEDs and the button
LED_PINS = [18, 24, 25, 12, 16]  # GPIO pins for the LEDs
BUTTON_PIN = 23  # GPIO pin for the button

# Setup GPIO pins
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Ensure all LEDs are initially off

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Predefined material codes
PREDEFINED_MATERIALS = ["3MC10XYZ", "3MC20ABC", "3MC30DEF", "3MC40GHI", "3MC50JKL"]  # Replace with your material codes

def light_up_leds_and_wait_for_confirmation(matched_materials):
    for i, material in enumerate(matched_materials):
        if material in PREDEFINED_MATERIALS:
            GPIO.output(LED_PINS[i], GPIO.HIGH)  # Turn on the corresponding LED
            print(f"LED {i+1} is ON for material {material}. Waiting for button press...")

            # Wait for the button press
            while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                time.sleep(0.1)  # Debounce delay

            print(f"Button pressed. LED {i+1} will turn OFF.")
            GPIO.output(LED_PINS[i], GPIO.LOW)  # Turn off the corresponding LED

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
