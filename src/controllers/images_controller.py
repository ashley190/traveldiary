from models.Image import Images
from models.User import User
from schemas.ImageSchema import image_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort, current_app, Response
from pathlib import Path
from main import db
import boto3


images = Blueprint("images", __name__, url_prefix = "/<int:userid>/image")

@images.route("/", methods=["POST"])
@jwt_required
def create_user_image(userid):
    user = User.query.filter_by(userid=get_jwt_identity())

    if user.count() != 1:
        return abort(401, description="Invalid user")
    
    if "image" not in request.files:
        return abort(400, description="No image")

    image = request.files["image"]

    if Path(image.filename).suffix not in [".jpg", ".jpeg", ".png", ".tif", ".gif"]:
        return abort(400, description="Invalid file type")

    filename = f"{userid}{Path(image.filename).suffix}"
    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    key = f"user_images/{filename}"
    bucket.upload_fileobj(image, key)

    if not (user[0].image):
        new_image = Images()
        new_image.filename = filename
        user[0].image = new_image
        db.session.commit()
    
    return ("", 200)
    # if "image" in request.files:
    #     image = request.files["image"]
    #     image.save("uploaded_images/file_1")
    #     return ("", 200)
    # return abort(400, description="No image")

@images.route("/<int:imageid>", methods=["GET"])
def show_user_image(userid, imageid):
    image = Images.query.filter_by(imageid=imageid, user_id=userid).first()

    if not image:
        return abort(404, description="No image found")
    
    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    filename = image.filename
    file_obj = bucket.Object(f"user_images/{filename}").get()

    return Response(
        file_obj["Body"].read(),
        mimetype="image/*",
        headers={"Content-Disposition": f"attachment;filename=image"}
    )

@images.route("/<int:imageid>", methods=["DELETE"])
@jwt_required
def delete_user_image(userid, imageid):
    user = User.query.filter_by(userid=get_jwt_identity()).first()

    if not user:
        return abort(401, description="Invalid user")
    
    if user.image:
        bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
        filename = user.image.filename

        bucket.Object(f"user_images/{filename}").delete()

        db.session.delete(user.image)
        db.session.commit()
    
    return jsonify("successfully removed")