from flask import Flask
from authentification.authentification import authentification

app = Flask(__name__)
app.register_blueprint(authentification)


@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

if __name__ == "__main__":
    app.run()