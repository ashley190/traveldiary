from main import db
from models.Blog import Blog
from models.Review import Review


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    blogs = db.relationship(Blog, backref="user", lazy="dynamic")
    reviews = db.relationship(Review, backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.email}"
