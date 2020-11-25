from main import db


class Review(db.Model):
    __tablename__ = "reviews"

    reviewid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    location = db.Column(db.String())
    date = db.Column(db.Date())
    category = db.Column(db.String())
    activity_type = db.Column(db.String())
    rating = db.Column(db.Integer)
    description = db.Column(db.String())
    likes = db.Column(db.Integer)
