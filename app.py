from bottle import default_app, get, run, view, request, route, template, response
import time
import random
import sqlite3
#from django.shortcuts import render
import requests
import jwt

#   https://realpython.com/python-send-email/

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from get_email import sender_email
from get_password import password
from get_receiver_mail import receiver_email


################

def jwtfunction():
    cpr = "12345"
    iat = int(time.time())
    exp = iat + 600
    encoded_jwt = jwt.encode(
        {"cpr": cpr, "iat": iat, "exp": exp}, "serect", algorithm="HS256")
    print(encoded_jwt)
    return encoded_jwt

##############


@route("/")
def __():
    jwt = jwtfunction()
    return template("index", jwtData=jwt)

###############################


@route("/token")
def __():
    jwt = jwtfunction()
    return template("token", jwtData=jwt)
#######################


sender_email = sender_email
receiver_email = receiver_email
password = password

@route("/get_token", method="POST")
def get_jwtToken():
    try:
        # request forms ensures that all the necessary details are provided,
        # so we can stay organized and capture the information we need to evaluate and execute the job.
        jwtToken = request.forms.get("jwtToken")

        print(jwtToken)
        jwt.decode(jwtToken, key="secret", algorithms="HS256")
    except:
        print("Invalid Token !")
#############################################################
# # Sending the four digits code to my phone number

#         # creating 4 digit randon numbers

#         fourDigits = random.randint(1111, 9999)
#         print(fourDigits)


#        # phone = request.forms.get("phone")
#         print(phone)

#     try:
#         payload = {"to_phone": phone,
#                    "message": fourDigits,
#                    "api_key": api_key}
#         req = requests.post("https://fatsms.com/send-sms", data=payload)

#     except:
#         return req.status_code
#################################################################################
 
 #Sending the randondigits number to my mail id

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

 # database connection
 # cursor allows us to execute sql queries
   
        db = sqlite3.connect('SI_Mandatory_sendmail.db')
        c = db.cursor()
        db.execute("""CREATE TABLE IF NOT EXISTS randomDigitNumber(
                id INTEGER PRIMARY KEY NOT NULL,
                receiver_email VARCHAR(50) NOT NULL,
                random_auth_code VARCHAR(8))""")
        print(receiver_email, random_auth_code)

        db.execute(
            "INSERT INTO randomDigitNumber (receiver_email, random_auth_code) VALUES (?,?)", (receiver_email, random_auth_code))
        db.commit()

    # Show randon digit number in the page
    #c = db.cursor()
        c.execute("SELECT * FROM randomDigitNumber  ORDER BY ID DESC LIMIT 1 ")
        result = c.fetchone()
        print(result)
        return template('code')
        
    else:
        msg = "Something went wrong !"
        return msg

        db.close()
        
#################
# 4 digit number Varification

@route("/RandomDigitNumber", method="POST")
def randomDigits():
    try:
        otp = request.forms.get("randomDigitNumber")

        db = sqlite3.connect("SI_Mandatory_sendmail.db")
        c = db.cursor()
        c.execute(
            f"SELECT * FROM randomDigitNumber WHERE random_auth_code={otp}")
        print(otp)
        result = c.fetchone()
    except:
        return template("token")

    if result:
        print(result)
        return template("welcome")
    else:
        msg = "Wrong otp !"
        return msg


###################
try:
    import production
    application = default_app()
except:

    ###################
    run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")
