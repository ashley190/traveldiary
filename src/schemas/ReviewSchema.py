from main import ma
from models.Review import Review
from marshmallow.validate import Length, Range
from marshmallow import validates, ValidationError
from datetime import date
from schemas.UserSchema import UserSchema


class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review

    title = ma.String(validate=Length(min=1))
    location = ma.String(validate=Length(min=1))
    date = ma.Date()
    category = ma.String()
    activity_type = ma.String()
    rating = ma.Integer(validate=Range(max=5))
    description = ma.String(validate=Length(min=1))
    likes = ma.Integer()
    user = ma.Nested(UserSchema)    # doesn't work

    @validates("date")
    def not_future_date(*value):
        today = date.today()
        if value[1] > today:
            raise ValidationError("Invalid date.")


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
