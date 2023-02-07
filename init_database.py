from datetime import datetime
from sqlalchemy.exc import OperationalError

from config import app, db
from models import Win, Person, Game


def get_data_from_table(model):
    try:
        data = db.session.query(model).all()
        db.session.close()
        return data
    except OperationalError:
        return []


def create_database(db):
    db.create_all()
    db.session.commit()
    print("Created new database")


def update_database(db, existing_people, existing_wins):
    db.drop_all()
    db.create_all()
    for person in existing_people:
        db.session.merge(person)
    for win in existing_wins:
        db.session.merge(win)
    db.session.commit()
    print("Updated existing database")


with app.app_context():
    existing_people = get_data_from_table(Person)
    existing_wins = get_data_from_table(Win)

    if not existing_people:
        create_database(db)
    else:
        update_database(db, existing_people, existing_wins)
