from bottle import request, response, get, post, view, run, static_file
import jwt
from jwt.exceptions import InvalidSignatureError
import time

jwt_secret = "secret"
algorithm = "HS256"


##############################
@get("/images/mitid.png")
def _():
    return static_file("mitid.png", root="./images")


##############################
@get("/2fa")
@view("mitid")
def _():
    return

##############################
@get("/")
@view("jwt_stub")
def _():
    return


##############################
@post("/api-login")
def _():
    auth = request.headers.get('Authorization', None)
    if not auth:
        response.status = 403
        return {
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected'
        }

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        response.status = 403
        return {
            'code': 'invalid_header',
            'description': 'Authorization header must start with Bearer'
        }
    elif len(parts) == 1:
        response.status = 403
        return {'code': 'invalid_header', 'description': 'Token not found'}
    elif len(parts) > 2:
        response.status = 403
        return {
            'code': 'invalid_header',
            'description': 'Authorization header must be Bearer + \s + token'
        }

    try:
        print(parts[1])
        jwt.decode(parts[1], jwt_secret, algorithm)
        # TODO generate 4 digit code, send email and save email - code pair in DB
        return "OK"    
    except InvalidSignatureError:
        print("An exception occurred") 
        response.status = 403
        return {
            'code': 'invalid_signature',
            'description': 'Token signature is not valid'
        }

run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")
