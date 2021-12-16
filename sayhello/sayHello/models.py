from datetime import datetime
from sayhello.sayHello import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(1000))
    name = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
