from . import db

class Tag(db.Model): # type: ignore  [pyright thinking Model is wrong here]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  
