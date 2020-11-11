from main import db

class Blog(db.Model):
    __tablename__ = "blog"

    blogid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    date = db.Column(db.Date())
    location = db.Column(db.String())
    blog = db.Blog(db.Text())