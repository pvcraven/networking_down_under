# Import the built-in library that manages network sockets
import socket


# What IP address do you want to listen on?
# This should be the IP address of the computer you are running this
# program on. You can use 127.0.0.1 if you are connecting just to yourself.
listen_ip_address = '127.0.0.1'

# What port might the message come in on?
listen_ip_port = 10000

# How big might the message be?
buffer_size = 66000

# Create a networking socket to receive IP data (AF_INET)
# of type datagram (SOCK_DGRAM)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# "Bind" the socket to a particular IP address and port
s.bind((listen_ip_address, listen_ip_port))

while True:
    # Receive our data
    data, source_address = s.recvfrom(buffer_size)
    print("From {}:{}: {}".format(source_address[0], source_address[1], data))
