from flask import Blueprint, send_file, request
from analytics.models import UserActions
import os

blueprint = Blueprint('events', __name__)

@blueprint.route('/user-action')
def user_action():
    # TODO Track user actions (add more parameter)
    curr_path = os.path.dirname(os.path.abspath(__file__))
    img_path = '%s/../resources/1px.gif' % curr_path
    return send_file(img_path)
