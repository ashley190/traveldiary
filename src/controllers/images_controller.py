from models.Image import Images
from models.User import User
from schemas.ImageSchema import image_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort


images = Blueprint("images", __name__, url_prefix = "/<int:userid>/image")

@images.route("/", methods=["POST"])
@jwt_required
def create_user_image(userid):
    if "image" in request.files:
        image = request.files["image"]
        image.save("uploaded_images/file_1")
        return ("", 200)
    return abort(400, description="No image")

@images.route("/<int:imageid>", methods=["GET"])
def show_user_image(userid, imageid):
    pass

@images.route("/<int:imageid>", methods=["DELETE"])
@jwt_required
def delete_user_image(userid, imageid):
    pass