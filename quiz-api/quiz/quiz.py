from flask import Blueprint, request, jsonify
from . import models
from . import database
from tools import jwt_utils as jwt
from tools import create_db
import json
quiz = Blueprint("quiz", __name__)

@quiz.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@quiz.route('/rebuild-db', methods = ['POST'])
def init_db():
    raw_token = request.headers.get('Authorization')
    if raw_token == None : 
        return 'Missing authorization headers', 401
    token = raw_token.replace("Bearer ","")
    try : 
        try : 
            create_db.create_question(path = create_db.PATH)
            return "Ok", 200
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
        count = int(database.count_elements("question"))
        # print(payload)
        question = models.Question(
                            id = count,
                            title = payload["title"],
                            text = payload["text"],
                            image = payload["image"],
                            position = payload["position"],
                            possibleAnswers = payload["possibleAnswers"]
                        )
        print(question.toJson())
        print()
        print()
        print(payload)
        print(payload["possibleAnswers"])
        database.insert_question(question)
        return question.toJson(), 200
    except jwt.JwtError as e:
        print(e)
        return 'Unauthorized', 401

@quiz.route('/questions/<which>', methods=['DELETE'])
def delete_question(which) : 
    # check if the user wants to delete one question or all questions
    if which == "all" :
        question_id = "all"
    else : 
        try : 
            question_id = int(which)
        except : 
            return "Les valeurs possibles sont 'all' ou bien un nombre",401
    
    #Check if user is logged in
    raw_token = request.headers.get('Authorization')
    if raw_token == None : 
        return 'Missing authorization headers', 401
    token = raw_token.replace("Bearer ","")
    try : 
        jwt.decode_token(token)
        
        # once the users is authenticated + the questions he wants to delete (all or a number) is correct, we can delete question
        database.delete_question(question_id)
        return "No Content", 204
    except jwt.JwtError as e:
        print(e)
        return 'Unauthorized', 401

@quiz.route("/questions/<question_id>", methods=["GET"])
def get_question(question_id):
    question = database.retrieve_one_question(int(question_id))
    # question.possibleAnswers = json.loads(question.possibleAnswers)
    print(question.possibleAnswers)
    return question.toJson(), 200