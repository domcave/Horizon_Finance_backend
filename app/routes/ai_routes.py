from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user

auth_bp = Blueprint('ai', __name__)

@auth_bp.route('/generate_summary', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    return jsonify("test"), 200

