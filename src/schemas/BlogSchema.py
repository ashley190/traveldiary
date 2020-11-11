from main import ma
from models.Blog import Blog


class BlogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blog


blog_schema = BlogSchema()
