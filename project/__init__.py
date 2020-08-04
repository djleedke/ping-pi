from flask import Flask
import os

app = Flask(__name__)

try:
    from .local_settings import *
except ImportError:
    pass

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

from project import routes