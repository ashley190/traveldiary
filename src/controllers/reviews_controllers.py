from models.Review import Review
from main import db
from schemas.ReviewSchema import review_schema, reviews_schema
from flask import Blueprint, request, jsonify
reviews = Blueprint("reviews", __name__, url_prefix="/reviews")

@reviews.route("/", methods=["GET"])
def all_reviews():
    #View all reviews
    reviews = Review.query.all()
    return jsonify(reviews_schema.dump(reviews))

@reviews.route("/<int:id>", methods=["GET"])
def review_show(id):
    review = Review.query.get(id)
    return jsonify(review_schema.dump(review))

@reviews.route("/new_review", methods=["POST"])
def new_review():
    # Create review
    review_fields = review_schema.load(request.form)

    new_review = Review()
    new_review.location = review_fields["location"]
    new_review.date = review_fields["date"]
    new_review.category = review_fields["category"]
    new_review.activity_type = review_fields["activity_type"]
    new_review.rating = review_fields["rating"]
    new_review.description = review_fields["description"]
    new_review.likes = 0

    db.session.add(new_review)
    db.session.commit()

    return jsonify(review_schema.dump(new_review))

@reviews.route("/<int:id>", methods=["PUT"])
def review_update(id):
    # Update review
    review = Review.query.filter_by(reviewid=id)
    review_fields = review_schema.load(request.form)
    review.update(review_fields)
    db.session.commit()

    return jsonify(review_schema.dump(review[0]))

@reviews.route("/<int:id>", methods=["DELETE"])
def delete_review(id):
    # Delete review
    review = Review.query.get(id)
    db.session.delete(review)
    db.session.commit()

    return jsonify(review_schema.dump(review))

@reviews.route("/<int:id>/like", methods=["PATCH"])
def like_review(id):
    review = Review.query.filter_by(reviewid=id)

    return jsonify(review_schema.dump(review[0]))

@reviews.route("/<int:id>/comment", methods=["PATCH"])
def review_comment(id):
    return f"Comment on review id:{id}"