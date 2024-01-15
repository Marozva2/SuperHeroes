from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

hero_powers = db.Table('hero_powers',
    db.Column('hero_id', db.Integer, db.ForeignKey('hero.id'), primary_key=True),
    db.Column('power_id', db.Integer, db.ForeignKey('power.id'), primary_key=True)
)

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    powers = db.relationship('Power', secondary=hero_powers, lazy='subquery',
                             backref=db.backref('heroes', lazy=True))

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

class HeroPower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'))
    strength = db.Column(db.String)
    hero = db.relationship('Hero', backref=db.backref('hero_powers'))
    power = db.relationship('Power', backref=db.backref('hero_powers'))
