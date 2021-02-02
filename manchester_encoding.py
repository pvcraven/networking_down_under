"""
Manchester Encoding

Sends a message across a wire using Manchester Encoding.
"""

import time
import RPi.GPIO as GPIO

# Data channel to transmit on
DATA_CHANNEL = 12

# Speed between transitions
CLOCK_SPEED = .005

BITS_IN_A_BYTE = 8

# Setup the pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_CHANNEL, GPIO.OUT)

# Put the pin high so we have a known starting state, and
# wait for a bit, so we know this isn't part of the message
GPIO.output(DATA_CHANNEL, GPIO.HIGH)
time.sleep(CLOCK_SPEED * 4)

GPIO.output(DATA_CHANNEL, GPIO.LOW)
time.sleep(CLOCK_SPEED * 4)

# The Message
my_message = b'This is a secret message'

# Loop through each letter/byte in the message
for my_byte in my_message:

    # Loop through each bit in the byte.
    # Starting at 7 down to 0
    for bit_pos in range(BITS_IN_A_BYTE - 1, -1, -1):

        # Take a 1 and shift into our bit position.
        # Compare to the data, any value left means we have a 1 in that position
        # 0100 0000

        bit = (1 << bit_pos) & my_byte

        # A 1 could be 1, 2, 4, 8, 16, 32, 64, or 128 position
        if bit != 0:
            # A one is represented by a low to high transition
            # Go low, wait, go high, wait
            GPIO.output(DATA_CHANNEL, GPIO.LOW)
            time.sleep(CLOCK_SPEED)
            print("1", end='')
            GPIO.output(DATA_CHANNEL, GPIO.HIGH)
            time.sleep(CLOCK_SPEED)
        else:
            # A zero is represented by a high to low transition
            # Go high, wait, go low, wait
            GPIO.output(DATA_CHANNEL, GPIO.HIGH)
            time.sleep(CLOCK_SPEED)
            print("0", end='')
            GPIO.output(DATA_CHANNEL, GPIO.LOW)
            time.sleep(CLOCK_SPEED)

    # print(bit, end="")
    print(" - {:3} - {:}".format(my_byte, chr(my_byte)))

time.sleep(CLOCK_SPEED * 4)
GPIO.cleanup()

