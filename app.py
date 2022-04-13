from bottle import request, response, view, run, static_file, abort
import random
import jwt, bottle
from jwt.exceptions import InvalidSignatureError
from my_persistence import createDB, save_record, evaluate_code
from send_email import send_email

db_name = "sample.db"
jwt_secret = "secret"
algorithm = "HS256"
sender_email = "satestastos@gmail.com"
receiver_email = "sagelastos@gmail.com"
password = "panJr6Ujt4XVwb"

app = bottle.Bottle()
createDB(db_name)

##############################
@app.get("/images/mitid.png")
def image():
    return static_file("mitid.png", root="./images")


##############################
@app.post("/2fa")
@view("two_fa")
def two_fa():
    email = request.forms["email"]
    code = request.forms["code"]
    if evaluate_code(db_name, email, code):
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


##############################
@app.get("/")
@view("jwt_stub")
def index():
    return


##############################
@app.post("/api-login")
def jwt_validate():
    auth = request.headers.get("Authorization", None)
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
        print(parts[1])
        jwt.decode(parts[1], jwt_secret, algorithm)
        # TODO generate 4 digit code, send email and save email - code pair in DB
        code = random.randint(1000, 9999)
        save_record(db_name=db_name, email=receiver_email, code=code)
        send_email(
            sender_email=sender_email,
            password=password,
            receiver_email=receiver_email,
            random_auth_code=code,
        )
        return "OK"
    except InvalidSignatureError:
        print("An exception occurred")
        response.status = 403
        return {
            "code": "invalid_signature",
            "description": "Token signature is not valid",
        }


run(app, host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")
