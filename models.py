
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db=SQLAlchemy()
class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
    is_admin=db.Column(db.Boolean,default=False)
    active=db.Column(db.Boolean,default=True)
class Team(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    qr_code=db.Column(db.String(20),unique=True)
    track=db.Column(db.String(20)); team_name=db.Column(db.String(120))
    leader_name=db.Column(db.String(120)); roll=db.Column(db.String(50))
    institute=db.Column(db.String(150)); location=db.Column(db.String(120))
    phone=db.Column(db.String(20)); count=db.Column(db.Integer)
    members=db.relationship("Member",backref="team",cascade="all,delete")
class Member(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    team_id=db.Column(db.Integer,db.ForeignKey("team.id"))
    name=db.Column(db.String(120)); roll=db.Column(db.String(50)); phone=db.Column(db.String(20))
