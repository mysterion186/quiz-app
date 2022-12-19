from flask import Blueprint, request
from . import models
from . import database

quiz = Blueprint("quiz", __name__)

@quiz.route('/questions',methods=['POST'])
def add_questions() : 
    payload = request.get_json()
    question = models.Question(
                        title = payload["title"],
                        text = payload["text"],
                        image = payload["image"],
                        position = payload["position"],
                        possibleAnswer = payload["possibleAnswers"]
                    )
    database.insert_question(question)
    print("Après l'insertion")
    return "ok", 200