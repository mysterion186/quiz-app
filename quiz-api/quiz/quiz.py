from flask import Blueprint, request
from . import models
from . import database
from tools import jwt_utils as jwt
from tools import create_db
quiz = Blueprint("quiz", __name__)

@quiz.route('/rebuild-db', methods = ['POST'])
def init_db():
    raw_token = request.headers.get('Authorization')
    if raw_token == None : 
        return 'Missing authorization headers', 401
    token = raw_token.replace("Bearer ","")
    try : 
        try : 
            create_db.create_question(path = create_db.PATH)
            return "ok", 200
        except Exception as e :
            print(e)
            return "Error", 401
    except jwt.JwtError as e:
        print(e)
        return 'Unauthorized', 401

@quiz.route('/questions',methods=['POST'])
def add_questions() : 
    # headers = request.headers
    raw_token = request.headers.get('Authorization')
    if raw_token == None : 
        return 'Missing authorization headers', 401
    token = raw_token.replace("Bearer ","")
    try : 
        jwt.decode_token(token)
        payload = request.get_json()
        question = models.Question(
                            title = payload["title"],
                            text = payload["text"],
                            image = payload["image"],
                            position = payload["position"],
                            possibleAnswer = payload["possibleAnswers"]
                        )
        database.insert_question(question)
        return "ok", 200
    except jwt.JwtError as e:
        print(e)
        return 'Unauthorized', 401