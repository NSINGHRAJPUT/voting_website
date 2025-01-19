from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    voter_id = db.Column(db.String(100), unique=True, nullable=False)

    # Relationship with Votes
    votes = db.relationship('Vote', backref='user', lazy=True)

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    # Relationship with Votes
    votes = db.relationship('Vote', backref='election', lazy=True)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_vote'), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id', name='fk_election_vote'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
