from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import create_engine, MetaData
from logging.config import dictConfig
import os

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))
config = {}

if('environment' in os.environ and os.environ['environment'] == 'production'):
    config = os.environ
else:
    import json
    config = json.load(open('%s/../dev_config.json' % dir_path))

connection_string = config['CONNECTION_STRING']
engine = create_engine(connection_string)
metadata = MetaData(bind=engine)
db_conn = engine.connect()

import controllers, models, scheduled_tasks

# blueprints
from controllers import  auth, events
app.register_blueprint(auth.blueprint, url_prefix='')
app.register_blueprint(events.blueprint, url_prefix='/events')
