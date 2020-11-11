from flask_sqlalchemy import SQLAlchemy
import os

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://traveldiaryuser:{os.getenv('DB_PASSWORD')}@localhost:5432/traveldiary"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)
    return db