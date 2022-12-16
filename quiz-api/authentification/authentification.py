from flask import Blueprint
from flask import Flask, request
from jwt_utils import build_token


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
