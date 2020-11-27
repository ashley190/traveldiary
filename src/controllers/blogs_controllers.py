from models.Blog import Blog
from models.User import User
from main import db
from schemas.BlogSchema import blog_schema, blogs_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort

blogs = Blueprint('blogs', __name__, url_prefix="/blogs")


@blogs.route("/", methods=["GET"])
@jwt_required
def blog_index():
    # View all blog posts
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    blogs = Blog.query.filter_by(userid=user.id)

    if blogs.count() < 1:
        return abort(400, description="No blog posts found")

    return jsonify(blogs_schema.dump(blogs))


@blogs.route("/<int:id>", methods=["GET"])
@jwt_required
def blog_post(id):
    # View single blog post
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    blog = Blog.query.filter_by(blogid=id, userid=user.id).first()
    if not blog:
        return abort(401, description="Unauthorized to view this blog post")

    return jsonify(blog_schema.dump(blog))


@blogs.route("/", methods=["POST"])
@jwt_required
def blog_create():
    # Publish blog post
    blog_fields = blog_schema.load(request.form)
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    new_blog = Blog()
    new_blog.title = blog_fields["title"]
    new_blog.date = blog_fields["date"]
    new_blog.location = blog_fields["location"]
    new_blog.blog = blog_fields["blog"]

    user.blogs.append(new_blog)
    db.session.commit()

    return jsonify(blog_schema.dump(new_blog))


@blogs.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def blog_update(id):
    # Update blog post
    blog_fields = blog_schema.load(request.form)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    blog = Blog.query.filter_by(blogid=id, userid=user.id)

    if blog.count() != 1:
        return abort(401, description="Unauthorised to update this blog")

    blog.update(blog_fields)
    db.session.commit()

    return jsonify(blog_schema.dump(blog[0]))


@blogs.route("/<int:id>", methods=["DELETE"])
@jwt_required
def blog_delete(id):
    # Delete blog post
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    blog = Blog.query.filter_by(blogid=id, userid=user.id).first()

    if not blog:
        return abort(400, description="Unauthorised to delete blog")

    db.session.delete(blog)
    db.session.commit()

    return jsonify(blog_schema.dump(blog))
