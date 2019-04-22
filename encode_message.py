# Import libraries
import time
import RPi.GPIO as GPIO

# Constants
CLOCK_LINE_PIN = 17
DATA_LINE_PIN = 18
SLEEP_TIME = 0.1

# Set up our GPIO pins
GPIO.setmode(GPIO.BCM)

GPIO.setup(CLOCK_LINE_PIN, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

# Set up data
done = False
bits_in_a_byte = 8
my_message = b'Hello World'

# Loop through each byte of our message
for my_byte in my_message:

    # Loop for each bit of the byte
    for bit_pos in range(bits_in_a_byte):

        # Use a single 1, and bit shift it with << to the
        # spot we are interested in. Then use a bitwise
        # and to see if that spot has a value
        bit = (1 << bit_pos) & my_byte

        if bit != 0:
            # There was a value
            bit_value = 1
            print(bit_value)
        else:
            # There was not a value
            bit_value = 0
            print(bit_value)

        # Turn the clock line on
        GPIO.output(CLOCK_LINE_PIN, GPIO.HIGH)

        # Turn the data line on/off depending on our data
        if bit_value == 1:
            GPIO.output(DATA_LINE_PIN, GPIO.HIGH)
        else:
            GPIO.output(DATA_LINE_PIN, GPIO.LOW)

        # Wait
        time.sleep(SLEEP_TIME)

        # Turn the clock line off, signaling it is ok to read
        # the data line now that we aren't changing it
        GPIO.output(CLOCK_LINE_PIN, GPIO.LOW)

        # Wait
        time.sleep(SLEEP_TIME)
