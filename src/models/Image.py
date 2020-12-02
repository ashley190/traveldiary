from main import db


class Images(db.Model):
    __tablename__ = "images"

    imageid = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String())
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.userid"), nullable=False)

    def __repr__(self):
        return f"<Image {self.imageid}>"
