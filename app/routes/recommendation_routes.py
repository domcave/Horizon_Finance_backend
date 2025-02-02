from flask import Blueprint, request, jsonify
from flask_cors import CORS
import json
from app.init_services import ai_service, house_rec_service, marraige_rec_service, retirement_rec_service
from app.extensions import db
from app.models.user import User

rec_bp = Blueprint('recommendations', __name__)
CORS(rec_bp)


def getUserIncome(username):
    user_income = db.session.query(User).filter(User.username == username).first().income
    return user_income

def getUserAge(username):
    user_age = db.session.query(User).filter(User.username == username).first().age
    return user_age


@rec_bp.route("/house", methods=["GET"])
def getHouseRecommendation():
    '''
        Query Params:
            - username
            - owned_house_price
    '''
    try:
        for key, val in request.args.items():
            print(f"key: {key}, val: {val}")
        username = request.args.get("username")
        income = getUserIncome(username)
        owned_house_price = int(request.args.get("owned_house_price"))
        
        text = house_rec_service.get_recommendation(income, owned_house_price)
        text = json.dumps(text)
        response = ai_service.generate_summary(text)
        print(type(response))
        return jsonify({"recommendation": response}), 200
    except Exception as e:
        print(e)
        return jsonify({
            "error": "Some error when getting summarized recommendation",
            "full_error": e
        }), 400


@rec_bp.route("/marriage", methods=["GET"])
def getMarriageRecommendation():
    '''
        Query Params:
            - username
            - spouse_income
            - num_kids
            - save
            - arr (annual return rate)
            - years_to_college
    '''
    try:
        username = request.args.get("username")
        annual_income = getUserIncome(username)
        spouse_income = int(request.args.get("spouse_income"))
        num_kids = int(request.args.get("num_kids"))
        save = bool(request.args.get("save"))
        years_to_college = int(request.args.get("years_to_college"))
        arr = float(request.args.get("arr"))
        
        text = marraige_rec_service.get_recommend(spouse_income, annual_income, num_kids, save, years_to_college, arr)
        text = json.dumps(text)
        response = ai_service.generate_summary(text)
        return jsonify({"recommendation": response}), 200
    except Exception as e:
        print(e)
        return jsonify({
            "error": "Some error when getting summarized recommendation",
            "full_error": e
        }), 400


@rec_bp.route("/retirement", methods=["GET"])
def getRetirementRecommendation():
    '''
        Query Params:
            - username
            - savings
            - arr (annual return rate)
            - wd_rate (withdrawl_rate)
            - target_amount
    '''
    try:
        username = request.args.get("username")
        annual_income = getUserIncome(username)
        age = getUserAge(username)
        savings = int(request.args.get("savings"))
        arr = float(request.args.get("arr"))
        wd_rate = float(request.args.get("wd_rate"))
        target_amount = int(request.args.get("target_amount"))

        text = retirement_rec_service.calculate_retirement(age, savings, annual_income, arr, wd_rate)
        text = json.dumps(text)
        response = ai_service.generate_summary(text)
        return jsonify({"recommendation": response}), 200
    except Exception as e:
        print(e)
        return jsonify({
            "error": "Some error when getting summarized recommendation",
            "full_error": e
        }), 400

