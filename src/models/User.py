from main import db
from models.Blog import Blog
from models.Review import Review
from models.Image import Images


class User(db.Model):
    __tablename__ = "user"

    userid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String())
    age = db.Column(db.Integer)
    location = db.Column(db.String())
    interests = db.Column(db.String())
    about_me = db.Column(db.String())
    blogs = db.relationship(
        Blog, backref="user", lazy="dynamic",
        cascade="all, delete, delete-orphan")
    reviews = db.relationship(
        Review, backref="user", lazy="dynamic",
        cascade="all, delete, delete-orphan")
    image = db.relationship(
        Images, backref="user", uselist=False,
        cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}"
