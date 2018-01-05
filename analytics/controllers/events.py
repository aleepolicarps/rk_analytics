from flask import Blueprint, send_file, request
from analytics.models.user_action import UserAction
from analytics import session
import os

blueprint = Blueprint('events', __name__)

@blueprint.route('/user-action')
def user_action():
    user_action = UserAction()
    user_action.account = request.args.get('account')
    user_action.action = request.args.get('action')
    user_action.user_id = request.args.get('user_id')
    user_action.customer_id = request.args.get('customer_id')
    user_action.web_id = request.args.get('web_id')
    user_action.first_name = request.args.get('first_name')
    user_action.last_name = request.args.get('last_name')
    user_action.email = request.args.get('email')
    user_action.ip_address = request.remote_addr
    user_action.referrer_url = request.referrer
    user_action.session = request.args.get('session')
    user_action.section = request.args.get('section')
    user_action.subsection = request.args.get('subsection')
    user_action.value = request.args.get('value')
    user_action.utm_source = request.args.get('utm_source')
    user_action.utm_medium = request.args.get('utm_medium')
    user_action.utm_campaign = request.args.get('utm_campaign')
    user_action.utm_term = request.args.get('utm_term')
    user_action.utm_content = request.args.get('utm_contents')
    session.add(user_action)
    session.commit()

    curr_path = os.path.dirname(os.path.abspath(__file__))
    img_path = '%s/../resources/1px.gif' % curr_path
    return send_file(img_path)
