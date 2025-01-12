from flask_sqlalchemy import SQLAlchemy

def create_db():
    db = SQLAlchemy()

    return db

db = create_db()