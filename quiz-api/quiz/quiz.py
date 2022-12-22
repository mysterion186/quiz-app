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
            create_db.create_participation(path = create_db.PATH)
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
    print(which, type(which))
    if which == "all" :
        question_id = "all"
        code = ("No Content",204)
    else : 
        try : 
            question_id = int(which)
            code = ("No Content",204)
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
        if question_id != "all" : 
            question = database.retrieve_one_question(question_id)
            if question == None : 
                return "Not found",404
        database.delete_question(question_id)
        print(code)
        return code
    except jwt.JwtError as e:
        print(e)
        return 'Unauthorized', 401

@quiz.route("/questions/<question_id>", methods=["GET"])
def get_question(question_id):
    question = database.retrieve_one_question(int(question_id))
    # question.possibleAnswers = json.loads(question.possibleAnswers)
    if question == None : 
        return "Not Found",404
    return question.toJson(), 200

@quiz.route("/questions", methods=["GET"])
def get_questions_by_position():
    pos_id = int(request.args.get("position"))
    question = database.retrieve_one_question(pos_id, key="position")
    if question == None : 
        return "Not Found",404
    return question.toJson(), 200

@quiz.route("/questions/<question_id>", methods=["PUT"])
def update_question(question_id) : 
    #Check if user is logged in
    raw_token = request.headers.get('Authorization')
    if raw_token == None : 
        return 'Missing authorization headers', 401
    token = raw_token.replace("Bearer ","")
    try : 
        jwt.decode_token(token)
    except jwt.JwtError as e:
        print(e)
        return 'Unauthorized', 401

    payload = request.get_json()
    question = database.retrieve_one_question(int(question_id))
    if question == None :
        return "Not Found", 404
    # Update question, don't take in account the position handling error (position > number of questions)
    question.title = payload['title']
    question.image = payload["image"]
    question.text = payload["text"]
    question.position = payload["position"]
    question.possibleAnswers = payload["possibleAnswers"]
    database.update_question(question)
    return "No Content", 204
