from main import db


class Blog(db.Model):
    __tablename__ = "blog"

    blogid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    date = db.Column(db.Date())
    location = db.Column(db.String())
    blog = db.Column(db.Text())
    userid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
