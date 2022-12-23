from flask import Blueprint, request, jsonify
from . import models
from . import database
from tools import jwt_utils as jwt
from quiz import database as q_database
from datetime import datetime
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

@participation.route("/participations", methods=["POST"])
def participate():
    payload = request.get_json()
    number_question = q_database.count_elements("question") - 1
    player_name = payload["playerName"]
    answers = payload["answers"]
    if len(answers) != number_question : 
        return "Not same lenght", 400
    questions = q_database.retrieve_all_question(number_question + 1)
    score = 0
    for k in range(len(questions)):
        print(questions[k].possibleAnswers)
        print(answers[k])
        print(q_database.get_correct_answer_pos(questions[k]) == answers[k])
        print()
        if q_database.get_correct_answer_pos(questions[k]) == answers[k]:
            score += 1
    now = datetime.now()
    formatted_date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    participation = models.Participation(
        playerName= player_name,
        score=score,
        date= formatted_date_time
    )
    database.insert_participation(participation)
    return participation.toJson(), 200
    