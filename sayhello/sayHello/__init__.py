from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('sayHello')
db = SQLAlchemy(app)
app.config.from_pyfile('settings.py')

