import time
import RPi.GPIO as GPIO

DATA_CHANNEL = 12
MANCHESTER_INTERVAL = .005

GPIO.setmode(GPIO.BCM)

GPIO.setup(DATA_CHANNEL, GPIO.OUT)

bits_to_encode = 8

# The Message
my_message = b'Secret Message!'

for my_byte in my_message:

    for bit_pos in range(bits_to_encode):

        bit = (1 << bit_pos) & my_byte
        if bit != 0:
            GPIO.output(DATA_CHANNEL, GPIO.LOW)
            time.sleep(MANCHESTER_INTERVAL)
            print("1", end='')
            GPIO.output(DATA_CHANNEL, GPIO.HIGH)
            time.sleep(MANCHESTER_INTERVAL)
        else:
            GPIO.output(DATA_CHANNEL, GPIO.HIGH)
            time.sleep(MANCHESTER_INTERVAL)
            print("0", end='')
            GPIO.output(DATA_CHANNEL, GPIO.LOW)
            time.sleep(MANCHESTER_INTERVAL)

    # print(bit, end="")
    print(" - {:3} - {:}".format(my_byte, chr(my_byte)))

