from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)


if os.environ['env'] == 'dev':
    import dev_config
    config = dev_config.Config
elif os.environ['env'] == 'production':
    import prod_config
    config = prod_config.Config

connection_string = config.CONNECTION_STRING
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

import controllers, models

# blueprints
from controllers import  auth, events
app.register_blueprint(auth.blueprint, url_prefix='')
app.register_blueprint(events.blueprint, url_prefix='/events')

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.close()
