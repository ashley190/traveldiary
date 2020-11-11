from models.Blog import Blog
from main import db
from schemas.BlogSchema import blog_schema
from flask import Blueprint, request, jsonify
blog = Blueprint('blog', __name__, url_prefix="/blog")


@blog.route("/<int:id>", methods=["GET"])
def blog_post(id):
    # View single blog post
    blog = Blog.query.get(id)
    return jsonify(blog_schema.dump(blog))

# @blog.route("/", methods=["POST"])
# def blog_create():
#     # Publish blog post
#     pass

# @blog.route("/<int:id>", methods=["PUT", "PATCH"])
# def blog_update(id):
#     # Update blog post
#     pass

# @blog.route("/<int:id>", methods=["DELETE"])
# def blog_delete(id):
#     # Delete blog post
#     pass