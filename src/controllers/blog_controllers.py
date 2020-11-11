# from database import cursor, connection
from flask import Blueprint, request, jsonify
blog = Blueprint('blog', __name__, url_prefix = "/blog")

@blog.route("/", methods=["POST"])
def blog_create():
    # Publish blog post
    pass

@blog.route("/<int:id>", methods=["GET"])
def blog_post(id):
    # View single blog post
    pass

@blog.route("/<int:id>", methods=["PUT", "PATCH"])
def blog_update(id):
    # Update blog post
    pass

@blog.route("/<int:id>", methods=["DELETE"])
def blog_delete(id):
    # Delete blog post
    pass