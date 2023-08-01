from db import db


class FrictionModel(db.Model):
    __tablename__ = "frictions"

    id = db.Column(db.Integer, primary_key=True)
    init_velocity = db.Column(db.Float(precision=32), unique=False, nullable=False)
    gravity = db.Column(db.Float(precision=32), unique=False, nullable=False)
    coef_friction = db.Column(db.Float(precision=32), unique=False, nullable=False)
