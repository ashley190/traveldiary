from models.User import User
from schemas.UserSchema import user_schema
from main import db, bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
from flask import Blueprint, request, jsonify, abort


user = Blueprint('users', __name__, url_prefix="/user")


@user.route("/register", methods=["POST"])
def user_register():
    user_fields = user_schema.load(request.json)
    user = User.query.filter_by(email=user_fields["email"]).first()

    if user:
        return abort(400, description="Email already registered")

    user = User()
    user.email = user_fields["email"]
    user.password = bcrypt.generate_password_hash(
        user_fields["password"]).decode("utf-8")

    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))


@user.route("/login", methods=["POST"])
def user_login():
    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["email"]).first()

    if not user or not bcrypt.check_password_hash(
            user.password, user_fields["password"]):
        return abort(401, description="Incorrect username and password")

    expiry = timedelta(days=1)
    access_token = create_access_token(
        identity=str(user.id), expires_delta=expiry)

    return jsonify({"token": access_token})
