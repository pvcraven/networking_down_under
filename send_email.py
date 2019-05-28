import smtplib
import ssl

# Note, GMail considers this a "less secure" application.
# If you use gmail, it will not accept this e-mail until you
# enable less secure applications on that account
port = 465
server_name = "smtp.gmail.com"

username = input("Enter your username: ")
password = input("Type your password: ")
destination_address = input("Enter destination email address: ")
subject = input("Enter subject line: ")
message = input("Enter message: ")

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(server_name, port, context=context) as server:
    server.login(username, password)
    server.sendmail(username, destination_address, message)
