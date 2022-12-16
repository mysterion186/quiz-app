from flask import Blueprint

authentification = Blueprint("authentification", __name__)


@authentification.route('/auth')
def test_authentication() : 
    x = "auth"
    return f"Hello, {x}" 