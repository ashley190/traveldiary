from main import ma
from models.Review import Review
from marshmallow.validate import Length, Range
from marshmallow import validates, ValidationError
from datetime import date


class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review

    location = ma.String(required=True, validate=Length(min=1))
    date = ma.Date(required=True)
    category = ma.String(required=True)
    activity_type = ma.String(required=True)
    rating = ma.Integer(required=True, validate=Range(max=5))
    description = ma.String(required=True, validate=Length(min=1))
    likes = ma.Integer()

    @validates("date")
    def not_future_date(*value):
        today = date.today()
        if value[1] > today:
            raise ValidationError("Invalid date.")


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
