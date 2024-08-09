import RPi.GPIO as GPIO
import pandas as pd
import time

# Configure the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define the pins connected to the LEDs
led_pins = [17, 27, 22, 10, 9, 11]  # Change these according to your setup
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)

# Function to light up LEDs based on the data
def display_leds(color_codes):
    for i, color in enumerate(color_codes):
        if i < len(led_pins):
            if color.strip().lower() == 'on':
                GPIO.output(led_pins[i], GPIO.HIGH)
            else:
                GPIO.output(led_pins[i], GPIO.LOW)
    time.sleep(2)  # Wait for 2 seconds before moving to the next set of colors

try:
    # Read the Excel file
    df = pd.read_excel('differences.xlsx', sheet_name='Différences')  # Replace with your file path and sheet name

    # Loop through each row and control the LEDs
    for index, row in df.iterrows():
        # Assuming each row has a 'Color' column with values like 'on,off,on'
        color_codes = row['Color'].split(',')  # Adjust based on your file's actual format
        display_leds(color_codes)

finally:
    # Clean up GPIO settings
    GPIO.cleanup()
