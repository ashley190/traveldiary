from main import ma
from models.Blog import Blog
from marshmallow.validate import Length
from marshmallow import validates, ValidationError
from datetime import date


class BlogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blog

    title = ma.String(required=True, validate=Length(min=1))
    date = ma.Date(required=True)
    location = ma.String(required=True, validate=Length(min=1))
    blog = ma.String(required=True, validate=Length(min=1))

    @validates("date")
    def not_future_date(*value):
        today = date.today()
        if value[1] > today:
            raise ValidationError("Invalid date.")


blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)
