
import datetime
from application import db
import datetime

class Website(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column(db.String(), nullable=False)
    job_type = db.Column(db.String(10), nullable=False)
    hours = db.Column(db.Integer(), nullable=False, default=0)
    minutes = db.Column(db.Integer(), nullable=False, default=0)
    seconds = db.Column(db.Integer(), nullable=False, default=0)
    last_ping = db.Column(db.DateTime, default=datetime.datetime.now())
