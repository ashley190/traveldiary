from main import ma
from models.User import User
from marshmallow.validate import Length


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ["password"]

    email = ma.String(required=True, validate=Length(min=4))
    password = ma.String(required=True, validate=Length(min=6))


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class ProfileSchema(UserSchema):
    email = ma.String()
    password = ma.String()
    name = ma.String(validate=Length(min=1))
    age = ma.Integer()
    location = ma.String()
    interests = ma.String()
    about_me = ma.String()


profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)
