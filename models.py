from datetime import datetime

from marshmallow_sqlalchemy import fields

from config import db, ma


class Win(db.Model):
    __tablename__ = "win"
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))
    comment = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class WinSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Win
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), nullable=False)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    wins = db.relationship(
        Win,
        backref="person",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Win.timestamp)",
    )


class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    wins = fields.Nested(WinSchema, many=True)


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    num_players = db.Column(db.Integer, nullable=False)
    play_time = db.Column(db.String(32))
    genre = db.Column(db.String(64))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    wins = db.relationship(
        Win,
        backref="game",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Win.timestamp)",
    )


class GameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Game
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    wins = fields.Nested(WinSchema, many=True)


person_schema = PersonSchema()
people_schema = PersonSchema(many=True)
win_schema = WinSchema()
game_schema = GameSchema()
