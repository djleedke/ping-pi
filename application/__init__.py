from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

try:
    from .local_settings import *
except ImportError:
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
db = SQLAlchemy(app)

from application.ping_pi import PingPi
ping_pi = PingPi(db)
ping_pi.start_pinging()

from application import routes