from bottle import request, response, view, run, static_file
from dotenv import load_dotenv
import os
import random
import jwt, bottle
import twofa
from jwt.exceptions import InvalidSignatureError
from send_email import send_email

# READ ENV VARS
load_dotenv()
mitid_url = os.environ.get("mitid_url")
jwt_secret = os.environ.get("jwt_secret")
algorithm = os.environ.get("algorithm")
sender_email = os.environ.get("sender_email")
receiver_email = os.environ.get("receiver_email")
password = os.environ.get("password")
port = os.environ.get("port")

app = bottle.Bottle()


##############################
@app.get("/")
@view("index")
def index():
    return dict(mitid_url=mitid_url)

# def validate_jwt(request, response):
    

# def get_cpr():


##############################
@app.post("/validate")
def _():
    auth = request.headers.get("Authorization", None)
    print(f"AUTH {auth}")
    if not auth:
        response.status = 403
        return {
            "code": "authorization_header_missing",
            "description": "Authorization header is expected",
        }

    parts = auth.split()

    if parts[0].lower() != "bearer":
        response.status = 403
        return {
            "code": "invalid_header",
            "description": "Authorization header must start with Bearer",
        }
    elif len(parts) == 1:
        response.status = 403
        return {"code": "invalid_header", "description": "Token not found"}
    elif len(parts) > 2:
        response.status = 403
        return {
            "code": "invalid_header",
            "description": "Authorization header must be Bearer + \s + token",
        }

    try:
        jwt.decode(parts[1], jwt_secret, algorithm)
        # TODO generate 4 digit code, send email and save email - code pair in DB
        code = random.randint(1000, 9999)
        twofa.save_record(email=receiver_email, code=code)
        # send_email(
        #     sender_email=sender_email,
        #     password=password,
        #     receiver_email=receiver_email,
        #     random_auth_code=code,
        # )
        return "OK"
    except InvalidSignatureError:
        response.status = 403
        return {
            "code": "invalid_signature",
            "description": "Token signature is not valid",
        }


##############################
@app.post("/twofa")
@view("two_fa")
def two_fa():
    email = request.forms["email"]
    code = request.forms["code"]
    if twofa.evaluate_code(email, code):
        return
    else:
        response.status = 403
        return {
            "code": "invalid_auth_code",
            "description": "Wrong authorization code",
        }


##############################
@app.get("/2fa")
@view("two_fa")
def two_fa():
    return


##############################
@app.get("/secret_page")
@view("secret_page")
def two_fa():
    return


try:
    import production

    application = app
except Exception as ex:
    run(app, host="127.0.0.1", port=port, debug=True, reloader=True, server="paste")
