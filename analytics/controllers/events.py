from flask import Blueprint, send_file, request
from analytics.models import BackendEvent
from analytics import db_conn
from datetime import datetime
import os

blueprint = Blueprint('events', __name__)


@blueprint.route('/user-action')
def user_action():
    curr_path = os.path.dirname(os.path.abspath(__file__))
    img_path = '%s/../resources/1px.gif' % curr_path
    return send_file(img_path)


@blueprint.route('/backend-event')
def backend_event():
    account = request.args.get('account')
    event = request.args.get('event')
    created_at = datetime.utcnow()
    value = request.args.get('value')
    status = request.args.get('status')
    db_conn.execute(BackendEvent.insert(), account=account, event=event, created_at=created_at, value=value, status=status)

    curr_path = os.path.dirname(os.path.abspath(__file__))
    img_path = '%s/../resources/1px.gif' % curr_path
    return send_file(img_path)
