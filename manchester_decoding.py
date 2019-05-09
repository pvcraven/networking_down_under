"""
Manchester Decoding

Receives a message sent by Manchester Encoding
"""
import time
import RPi.GPIO as GPIO

DATA_IN = 13
CLOCK_SPEED = .005

def data_callback(channel):
    time_interval = time.time() - data_callback.last_call
    data_bit = False

    if time_interval > CLOCK_SPEED + CLOCK_SPEED / 2:
        data_bit = False

    if time_interval > CLOCK_SPEED + CLOCK_SPEED / 2 or data_bit:
        if GPIO.input(channel):

            bit = GPIO.input(channel)
            my_bit = 1 << (7 - data_callback.numberOfBits)
            data_callback.result_byte += my_bit

            print("1", end='')
            data_callback.last_call = time.time()
            data_callback.numberOfBits += 1
        else:
            print("0", end='')
            data_callback.last_call = time.time()

            data_callback.numberOfBits += 1
    else:
        data_bit = True

    if data_callback.numberOfBits == 8:
        print(" - {:3} - {:}".format(data_callback.result_byte,
                                     chr(data_callback.result_byte)))
        data_callback.numberOfBits = 0
        data_callback.result_byte = 0

data_callback.numberOfBits = 0
data_callback.result_byte = 0
data_callback.last_call = time.time()

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_IN, GPIO.IN)

GPIO.add_event_detect(DATA_IN, GPIO.BOTH, callback=data_callback)

print("Running")
while True:
    time.sleep(10)

