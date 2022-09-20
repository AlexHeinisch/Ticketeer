from extensions import db

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
