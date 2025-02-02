from flask import Blueprint, request
from app.extensions import db
from app.models.user import User
from flask_cors import CORS

user_bp = Blueprint("user", __name__)

CORS(user_bp)

@user_bp.route("/profile", methods=["GET"])
def profile():
    return {"message": "User profile"}

@user_bp.route("/add_income_and_age", methods=["POST"])
def add_income_and_age():
    data = request.get_json()
    income = data.get("income")
    age = data.get("age")
    username = data.get("username")
    user = db.session.query(User).filter_by(username=username).first()
    user.income = income
    user.age = age
    db.session.commit()
    return {"message": "Income and age added"}
