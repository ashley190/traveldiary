from main import ma
from models.Blog import Blog
from marshmallow.validate import Length
from marshmallow import validates, ValidationError
from datetime import date
from schemas.UserSchema import UserSchema


class BlogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blog

    title = ma.String(validate=Length(min=1))
    date = ma.Date()
    location = ma.String(validate=Length(min=1))
    blog = ma.String(validate=Length(min=1))
    user = ma.Nested(UserSchema)

    @validates("date")
    def not_future_date(*value):
        today = date.today()
        if value[1] > today:
            raise ValidationError("Invalid date.")


blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)
