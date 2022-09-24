from ticketeer import db

class Tag(db.Model): # type: ignore  [pyright thinking Model is wrong here]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  

class User(db.Model): # type: ignore
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(100))

    def __init__(self, username) -> None:
        super().__init__()
        self.username = username
