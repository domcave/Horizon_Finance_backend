from flask import Blueprint, request, jsonify
from app.init_services import auth_service

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    result, status_code = auth_service.register_user(username, email, password, first_name=first_name, last_name=last_name)

    return jsonify(result), status_code


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    result, status_code = auth_service.login_user(email, password)

    return jsonify(result), status_code
