import arcade
import random
import socket

INITIAL_SCREEN_WIDTH = 800
INITIAL_SCREEN_HEIGHT = 600
SCREEN_TITLE = "Networked Bouncing Balls"

BUFFER_SIZE = 65536

# Left or right computer?
m = "left"


if m == "right":
    # Listen to the listed listed address and port for incoming
    # balls. Set to None if we aren't listening.
    listen_right = None
    listen_left = ('127.0.0.1', 10001)

    # Try to send the ball to the address and port if it
    # hits the edge. Set to None if it doesn't go anywhere.
    send_left = ('127.0.0.1', 10002)
    send_right = None
else:
    listen_right = ('127.0.0.1', 10002)
    listen_left = None
    send_left = None
    send_right = ('127.0.0.1', 10001)


# Set up the sockets for receiving data
if listen_left:
    left_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    left_socket.settimeout(0.0)
    left_socket.bind(listen_left)
    left_socket.listen(1)

if listen_right:
    right_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    right_socket.settimeout(0.0)
    right_socket.bind(listen_right)
    right_socket.listen(1)


class Ball:
    """ This class holds the info about our bouncing ball. """
    def __init__(self):
        self.center_x = 0
        self.center_y = 0
        self.change_x = 0
        self.change_y = 0
        self.radius = 0
        self.color = None

    def move(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y,
                                  self.radius, self.color)


class MyGame(arcade.Window):
    """ Main application class. """
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)

        arcade.set_background_color(arcade.color.LIGHT_GRAY)
        self.ball_list = []

    def create_ball(self):
        """ Create a random ball on the screen. """
        ball = Ball()

        # Create a random color, radius, and position
        # ball.color = (random.randrange(256), random.randrange(256), random.randrange(256))
        ball.color = (0, 0, 0)
        ball.radius = random.randrange(20, 41)
        ball.center_x = random.randrange(self.width)
        ball.center_y = random.randrange(self.height)

        # Loop until the ball isn't stationary
        while ball.change_x == 0 and ball.change_y == 0:
            ball.change_x = random.randrange(-5, 6)
            ball.change_y = random.randrange(-5, 6)

        return ball


    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()

        # Draw each ball
        for ball in self.ball_list:
            ball.draw()

    def send_ball(self, ball, connection_info):
        """ Make a network call to send the ball out over the network."""

        # Create the message
        my_message = f"{ball.center_x},{ball.center_y}," \
            f"{ball.change_x},{ball.change_y}," \
            f"{ball.radius}," \
            f"{ball.color[0]},{ball.color[1]},{ball.color[2]}"

        # Convert the message to a byte array that our socket expects.
        my_message_bytes = my_message.encode()

        # Send the data
        print(f"Send {my_message}")

        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_socket.connect(connection_info)
        send_socket.sendall(my_message_bytes)
        send_socket.close()
        print("Sent")

        # Remove the ball from the list
        self.ball_list.remove(ball)

    def receive_ball(self, my_socket):
        ball = None
        try:
            # Accept a connection on the socket
            connection, client_address = my_socket.accept()

            # Retrieve the data
            data = connection.recv(BUFFER_SIZE)

            # Close the connection
            connection.close()

            # Decode the byte array into a regular UTF-8 string
            my_string = data.decode("UTF-8")
            print("Got data:", my_string)

            # Split the data into a list based on a comma
            my_data = my_string.split(",")

            # Create the ball, and set the fields. Convert the items into
            # an integer before setting the fields.
            ball = Ball()
            ball.color = (int(my_data[5]), int(my_data[6]), int(my_data[7]))
            ball.radius = int(my_data[4])
            ball.center_x = int(my_data[0])
            ball.center_y = int(my_data[1])
            ball.change_x = int(my_data[2])
            ball.change_y = int(my_data[3])

        except BlockingIOError:
            pass

        # Return the ball variable
        return ball

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        for ball in self.ball_list:
            ball.move()

            if ball.change_x < 0 and ball.center_x - ball.radius < 0:
                if send_left is None:
                    ball.change_x *= -1
                else:
                    try:
                        print("Send left")
                        self.send_ball(ball, send_left)
                    except:
                        ball.change_x *= -1
                        print("Failed to send")

            if ball.change_x > 0 and ball.center_x + ball.radius > self.width:
                if send_right is None:
                    ball.change_x *= -1
                else:
                    try:
                        print("Send right")
                        self.send_ball(ball, send_right)
                    except:
                        ball.change_x *= -1
                        print("Failed to send")

            if ball.change_y < 0 and ball.center_y - ball.radius < 0:
                ball.change_y *= -1
            if ball.change_y > 0 and ball.center_y + ball.radius > self.height:
                ball.change_y *= -1

        # See if we have any incoming balls from the left
        if listen_left:
            ball = self.receive_ball(left_socket)
            if ball:
                print("Receive left")
                ball.center_x = 0
                self.ball_list.append(ball)

        # See if we have any incoming balls from the right
        if listen_right:
            ball = self.receive_ball(right_socket)
            if ball:
                print("Receive right")
                ball.center_x = self.width
                self.ball_list.append(ball)

    def on_key_press(self, key, key_modifiers):
        """ Called whenever a key on the keyboard is pressed. """
        
        # Spawn a new ball with a space
        if key == arcade.key.SPACE:
            ball = self.create_ball()
            self.ball_list.append(ball)

        # Quit with a Q
        if key == arcade.key.Q:
            exit()

        # Flip between full/windowed with F
        if key == arcade.key.F:
            # User hits s. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Instead of a one-to-one mapping, stretch/squash window to match the
            # constants. This does NOT respect aspect ratio. You'd need to
            # do a bit of math for that.
            self.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

def main():
    """ Main method """
    MyGame(INITIAL_SCREEN_WIDTH, INITIAL_SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
