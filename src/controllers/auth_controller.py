from flask import Blueprint


user = Blueprint('user', __name__, url_prefix="/user")


@user.route("/register", methods=["POST"])
def auth_register():
    return "working"
