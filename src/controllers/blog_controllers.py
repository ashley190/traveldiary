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


@blog.route("/", methods=["POST"])
def blog_create():
    # Publish blog post
    blog_fields = blog_schema.load(request.form)

    new_blog = Blog()
    new_blog.title = blog_fields["title"]
    new_blog.date = blog_fields["date"]
    new_blog.location = blog_fields["location"]
    new_blog.blog = blog_fields["blog"]

    db.session.add(new_blog)
    db.session.commit()

    return jsonify(blog_schema.dump(new_blog))


@blog.route("/<int:id>", methods=["PUT", "PATCH"])
def blog_update(id):
    # Update blog post
    blog = Blog.query.filter_by(blogid=id)
    blog_fields = blog_schema.load(request.form)
    blog.update(blog_fields)
    db.session.commit()

    return jsonify(blog_schema.dump(blog[0]))


@blog.route("/<int:id>", methods=["DELETE"])
def blog_delete(id):
    # Delete blog post
    blog = Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()

    return jsonify(blog_schema.dump(blog))
