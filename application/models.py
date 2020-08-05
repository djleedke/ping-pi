from application import db

class Website(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column(db.String(), unique=True, nullable=False)
    job_type = db.Column(db.String(10), nullable=False)