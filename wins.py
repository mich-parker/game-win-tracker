from flask import abort, make_response

from config import db
from models import Win, Person, win_schema


def read_one(win_id):
    win = win.query.get(win_id)

    if win is not None:
        return win_schema.dump(win)
    else:
        abort(404, f"win with ID {win_id} not found")


def read_all():
    wins = Win.query.all()
    return win_schema.dump(wins)


def update(win_id, win):
    existing_win = win.query.get(win_id)

    if existing_win:
        update_win = win_schema.load(win, session=db.session)
        existing_win.content = update_win.content
        db.session.merge(existing_win)
        db.session.commit()
        return win_schema.dump(existing_win), 201
    else:
        abort(404, f"win with ID {win_id} not found")


def delete(win_id):
    existing_win = win.query.get(win_id)

    if existing_win:
        db.session.delete(existing_win)
        db.session.commit()
        return make_response(f"{win_id} successfully deleted", 204)
    else:
        abort(404, f"win with ID {win_id} not found")


def create(win):
    person_id = win.get("person_id")
    person = Person.query.get(person_id)

    if person:
        new_win = win_schema.load(win, session=db.session)
        person.wins.append(new_win)
        db.session.commit()
        return win_schema.dump(new_win), 201
    else:
        abort(404, f"Person not found for ID: {person_id}")
