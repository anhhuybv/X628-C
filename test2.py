from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("__name__")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://"postgres:123@localhost:5432/postgres'
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, )