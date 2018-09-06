from flask import (Blueprint)


blueprint = Blueprint('events', __name__)


@blueprint.route("/")
def hello():
    return "Hello World!"