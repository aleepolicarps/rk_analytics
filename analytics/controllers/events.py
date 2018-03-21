from flask import Blueprint, send_file, request
from analytics.models import BackendEvent, Emails
from analytics import db_conn
from datetime import datetime
from sqlalchemy import and_
import os

blueprint = Blueprint('events', __name__)


def __get_gif():
    curr_path = os.path.dirname(os.path.abspath(__file__))
    img_path = '%s/../resources/1px.gif' % curr_path
    return send_file(img_path)


@blueprint.route('/user-action')
def user_action():
    return __get_gif()


@blueprint.route('/backend-event')
def backend_event():
    account = request.args.get('account')
    event = request.args.get('event')
    created_at = datetime.utcnow()
    value = request.args.get('value')
    status = request.args.get('status')
    db_conn.execute(BackendEvent.insert(), account=account, event=event, created_at=created_at, value=value, status=status)

    return __get_gif()


@blueprint.route('/email-send')
def email_send():
    account = request.args.get('account')
    recipient = request.args.get('recipient')
    sender = request.args.get('sender')
    subject = request.args.get('subject')
    tracking_uuid = request.args.get('tracking_uuid')
    send_date = datetime.utcnow()

    db_conn.execute(Emails.insert(),
                    account=account,
                    recipient=recipient,
                    sender=sender,
                    subject=subject,
                    tracking_uuid=tracking_uuid,
                    send_date=send_date)

    return __get_gif()


@blueprint.route('/email-read')
def email_read():
    tracking_uuid = request.args.get('tracking_uuid')
    ip_address = request.remote_addr
    referrer_url = request.referrer
    read_date = datetime.utcnow()

    Emails.update()\
        .where(and_(Emails.c.tracking_uuid == tracking_uuid, Emails.c.read_date == None))\
        .values(ip_address=ip_address, referrer_url=referrer_url, read_date=read_date)\
        .execute()

    return __get_gif()
