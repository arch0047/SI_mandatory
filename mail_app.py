#   https://realpython.com/python-send-email/

import smtplib
import ssl
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from get_mail import sender_email
from get_password import password
from get_receiver_mail import receiver_email

sender_email = sender_email
receiver_email = receiver_email
password = password

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

random_auth_code = str(random.randint(100000, 999999))

message_to_user = f"User, your verification code is: {random_auth_code}"

print(type(message_to_user))

# Create the plain-text and HTML version of your message
text = f"""\
{message_to_user}
"""

html = f"""\
<html>
  <body>
    <p>
      Dear,<br>
      <b>{message_to_user}</b><br>
    </p>
  </body>
</html>
"""

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email (this is a context manager)
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    try:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as ex:
        print(ex)


# only send mail upto 30 may 2022