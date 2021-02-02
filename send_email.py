import smtplib
import ssl

# Note, GMail considers this a "less secure" application.
# If you use gmail, it will not accept this e-mail until you
# enable less secure applications on that account
port = 465
server_name = "smtp.gmail.com"

# Setting the debug level to 1 will output everything that is sent to,
# or recevied from the server
debug_level = 1

username = input("Enter your username: ")
password = input("Type your password: ")
destination_address = input("Enter destination email address: ")
subject = input("Enter subject line: ")
message = input("Enter message: ")

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(server_name, port, context=context) as server:
    server.set_debuglevel(debug_level)
    server.login(username, password)
    server.sendmail(username, destination_address, message)
