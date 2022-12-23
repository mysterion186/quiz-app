from flask import Blueprint, request, jsonify
from . import models
from . import database
from tools import jwt_utils as jwt
from tools import create_db
import json
from participations import database as p_database
quiz = Blueprint("quiz", __name__)

@quiz.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": database.count_elements("question") - 1, "scores": p_database.retrieve_all_participations()}, 200

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
        question_number = database.count_elements("question")
        database.update_position(None, question, question_number, "insert")
        return question.toJson(), 200
    except jwt.JwtError as e:
        print(e)
        return 'Unauthorized', 401

@quiz.route('/questions/<which>', methods=['DELETE'])
def delete_question(which) : 
    # check if the user wants to delete one question or all questions
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
        # print(code)
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
    previous_pos = question.position
    question_number = database.count_elements("question")
    # Update question, don't take in account the position handling error (position > number of questions)
    print("Avant update", question.toJson())
    question.title = payload['title']
    question.image = payload["image"]
    question.text = payload["text"]
    question.position = payload["position"]
    question.possibleAnswers = payload["possibleAnswers"]
    # database.update_question(question)
    print("Après update", question.toJson())
    print("Dans le put",previous_pos, question.position)
    if previous_pos != question.position :
        print("dans le put cas diff")
        database.update_position(previous_pos, question, question_number, "update")
    else : 
        print("else")
        database.update_question(question)
    return "No Content", 204
