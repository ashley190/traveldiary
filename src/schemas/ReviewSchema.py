from main import ma
from models.Review import Review

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)