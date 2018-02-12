from flask import Blueprint

blueprint = Blueprint('home', __name__)


@blueprint.route('/login')
def index():
    return 'hello'
