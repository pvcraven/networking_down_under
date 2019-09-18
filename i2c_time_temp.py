import time
import datetime
import Adafruit_LED_Backpack
import adafruit_bmp280
import busio
import board

DELAY = 2

# Create display instance on default I2C address (0x70) and bus number.
display = Adafruit_LED_Backpack.SevenSegment.SevenSegment()

# Alternatively, create a display with a specific I2C address and/or bus.
# display = Adafruit_LED_Backpack.SevenSegment.SevenSegment(address=0x74, busnum=1)

# Initialize the display. Must be called once before using the display.
display.begin()
display.set_brightness(15)

# Set up and initialize the temp sensor
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

while True:

    # Display temperature

    # Figure out the reading
    temp_c = bmp280.temperature
    temp_f = 9.0 / 5.0 * temp_c + 32

    # Make a string to display
    my_str = "{:4.1f}".format(temp_f)

    # Display the string
    display.clear()
    display.set_colon(False)
    display.print_number_str(my_str)
    display.write_display()

    # Pause
    time.sleep(DELAY)

    # Get the current time
    currentDT = datetime.datetime.now()
    hour = currentDT.hour
    minute = currentDT.minute
    if hour > 12:
        hour -= 12

    # Make a string to display
    my_str = "{:02}{:02}".format(hour, minute)

    # Display the string
    display.clear()
    display.print_number_str(my_str)
    display.set_colon(True)
    display.write_display()

    # Pause
    time.sleep(DELAY)
