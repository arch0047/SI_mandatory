from bottle import default_app, get, run, view, request, route, template, response
import time
import random
from get_api_key import api_key
from get_phone import phone
import sqlite3
import requests
import jwt


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


# @get("/get_token")
# @view("token")
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

# Sending the four digits code to my phone number

        # creating 4 digit randon numbers

        fourDigits = random.randint(1111, 9999)
        print(fourDigits)

       # phone = request.forms.get("phone")
        print(phone)

    try:
        payload = {"to_phone": phone,
                   "message": fourDigits,
                   "api_key": api_key}
        req = requests.post("https://fatsms.com/send-sms", data=payload)

    except:
        return req.status_code

    # database connection
    # cursor allows us to execute sql queries

    db = sqlite3.connect('SI_Mandatory.db')
    c = db.cursor()
  #  db.execute("""CREATE TABLE fourDigitNumber
  #            (
  #               id INTEGER PRIMARY KEY,
  #              phone VARCHAR(8),
  #             fourDigit VARCHAR(4))""")

    db.execute(
        f"INSERT INTO fourDigitNumber (phone, fourDigit) VALUES ({phone}, {fourDigits})")
    db.commit()

    # Show data
   # c = db.cursor()
    c.execute("SELECT * FROM fourDigitNumber  ORDER BY ID DESC LIMIT 1 ")
    result = c.fetchone()
    print(result)

    return template('code')

    # db.close()

 #################

 # Token Varification


@route("/4digitNumber", method="POST")
def fourDigits():
    try:
        otp = request.forms.get("fourDigits")

        db = sqlite3.connect("SI_Mandatory.db")
        c = db.cursor()
        c.execute(f"SELECT * FROM fourDigitNumber WHERE fourDigit={otp}")
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
