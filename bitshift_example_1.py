# This program prints out the bits in a number.

# How many bits should we encode. Usually 8, or some other multiple of 8
bits_to_encode = 8

# What number do we want to encode?
number_to_encode = 23

# You can also encode letters by using ord(), which fetches
# the value of the letter.
# number_to_encode = ord('X')

# Loop for each bit
for bit_pos in range(bits_to_encode):

    # Use a single 1, and bit shift it with << to the
    # spot we are interested in.
    bit = (1 << bit_pos) & number_to_encode
    if bit != 0:
        bit_value = 1
    else:
        bit_value = 0

    print(f"Bit position {bit_pos:2} is {bit_value} which is worth {bit:2}.")
