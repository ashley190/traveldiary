from main import db
from flask import Blueprint


db_commands = Blueprint("db-custom", __name__)


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created!")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables deleted!")


@db_commands.cli.command("seed")
def seed_db():
    from models.Blog import Blog
    from models.Review import Review
    from faker import Faker
    faker = Faker()

    for i in range(10):
        blog = Blog()
        blog.title = faker.catch_phrase()
        blog.date = faker.date_object()
        blog.location = f"{faker.city()}, {faker.country()}"
        blog.blog = faker.text()
        db.session.add(blog)

    db.session.commit()
    print("Blog table seeded")

    for i in range(10):
        review = Review()
        review.title = faker.sentence()
        review.location = f"{faker.city()}, {faker.country()}"
        review.date = faker.date_object()
        review.category = faker.word()
        review.activity_type = faker.word()
        review.rating = faker.random_int(min=0, max=5)
        review.description = faker.text()
        db.session.add(review)

    db.session.commit()
    print("Review table seeded")
