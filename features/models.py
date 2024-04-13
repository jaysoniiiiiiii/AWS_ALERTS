# from app import db

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AccountInfo(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    surname = db.Column(db.String(200))
    githubusername = db.Column(db.String(200))
    email = db.Column(db.String(200))
    accesskey = db.Column(db.String(200))
    secreteaccesskey = db.Column(db.String(200))
    password = db.Column(db.String(200), nullable=False)
    # confirm_password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<AccountInfo %r>' % self.id
