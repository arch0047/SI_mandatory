from bottle import request, get, post, view, run, static_file
import jwt
import time

jwt_secret = "rGNBXhixV3BbbC"
algorithm = "HS256"

cpr = "12345"
iat = int(time.time())
exp = iat + 600

encoded_jwt = jwt.encode({
    "cpr": cpr,
    "iat": iat,
    "exp": exp
}, jwt_secret, algorithm)


##############################
@get("/images/mitid.png")
def _():
    return static_file("mitid.png", root="./images")


##############################
@get("/")
@view("jwt_stub")
def _():
    return dict(token=encoded_jwt)


##############################
@post("/api-login")
def _():
    auth = request.headers.get('Authorization', None)
    if not auth:
        return {
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected'
        }

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        return {
            'code': 'invalid_header',
            'description': 'Authorization header must start with Bearer'
        }
    elif len(parts) == 1:
        return {'code': 'invalid_header', 'description': 'Token not found'}
    elif len(parts) > 2:
        return {
            'code': 'invalid_header',
            'description': 'Authorization header must be Bearer + \s + token'
        }

    content = jwt.decode(parts[1], jwt_secret, algorithm)
    print(content)
    return "OK"


run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")
