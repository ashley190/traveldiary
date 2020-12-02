from main import ma
from models.Image import Images
from marshmallow.validate import Length


class ImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Images

    filename = ma.String(required=True, validate=Length(min=1))


image_schema = ImageSchema()
images_schema = ImageSchema(many=True)
