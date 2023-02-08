from flask import abort, make_response

from config import db
from models import Game, Person, game_schema


def read_all():
    games = Game.query.all()
    return game_schema.dump(games)


def read_one(game_id):
    game = game.query.get(game_id)

    if game is not None:
        return game_schema.dump(game)
    else:
        abort(404, f"game with ID {game_id} not found")


def update(game_id, game):
    existing_game = game.query.get(game_id)

    if existing_game:
        update_game = game_schema.load(game, session=db.session)
        existing_game.content = update_game.content
        db.session.merge(existing_game)
        db.session.commit()
        return game_schema.dump(existing_game), 201
    else:
        abort(404, f"game with ID {game_id} not found")


def delete(game_id):
    existing_game = game.query.get(game_id)

    if existing_game:
        db.session.delete(existing_game)
        db.session.commit()
        return make_response(f"{game_id} successfully deleted", 204)
    else:
        abort(404, f"game with ID {game_id} not found")


def create(game):
    person_id = game.get("person_id")
    person = Person.query.get(person_id)

    if person:
        new_game = game_schema.load(game, session=db.session)
        person.games.append(new_game)
        db.session.commit()
        return game_schema.dump(new_game), 201
    else:
        abort(404, f"Person not found for ID: {person_id}")
