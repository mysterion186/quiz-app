from flask import Blueprint
from flask import Flask, request
from tools.jwt_utils import build_token, decode_token, JwtError


authentification = Blueprint("authentification", __name__)


@authentification.route('/auth')
def test_authentication() : 
    x = "auth"
    return f"Hello, {x}" 

@authentification.route('/login', methods = ['POST'])
def user():
    payload = request.get_json()
    password = payload["password"]
    if password == "flask2023" :
        return {"token": build_token() },200
    else :
        return 'Unauthorized', 401

@authentification.route('/logged',methods = ['POST'])
def check_authentication() : 
    headers = request.headers
    payload = request.get_json()
    raw_token = headers["Authorization"]
    token = raw_token.replace("Bearer ","")
    try : 
        decode_token(token)
        return "ok",200
    except JwtError as e:
        print(e)
        return 'Unauthorized', 401
    print(payload)