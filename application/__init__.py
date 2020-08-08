from flask import Flask
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

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
