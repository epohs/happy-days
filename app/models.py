from datetime import datetime
from app import login, db
from flask_login import UserMixin



@login.user_loader
def load_user(id):
    return User.query.get(int(id))



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    entries = db.relationship('Entry', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)



class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    val = db.Column(db.Integer)
    entry_type_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Entry {}>'.format(self.val)


