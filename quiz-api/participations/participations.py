from flask import Blueprint, request, jsonify
from . import models
from . import database
from tools import jwt_utils as jwt

participation = Blueprint('participation',__name__)


@participation.route("/participations/all", methods=["DELETE"])
def delete_all() : 
    #Check if user is logged in
    raw_token = request.headers.get('Authorization')
    if raw_token == None : 
        return 'Missing authorization headers', 401
    token = raw_token.replace("Bearer ","")
    try : 
        jwt.decode_token(token)
        database.delete_participation()
        return 'No Content', 204
    except jwt.JwtError as e:
        print(e)
        return 'Unauthorized', 401