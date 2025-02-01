from flask import Blueprint

user_bp = Blueprint("user", __name__)

@user_bp.route("/profile", methods=["GET"])
def profile():
    return {"message": "User profile"}
