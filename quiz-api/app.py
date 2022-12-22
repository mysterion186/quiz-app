from flask import Flask
from authentification.authentification import authentification
from quiz.quiz import quiz
from participations.participations import participation

app = Flask(__name__)
app.register_blueprint(authentification)
app.register_blueprint(quiz)
app.register_blueprint(participation)
@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

if __name__ == "__main__":
    app.run()