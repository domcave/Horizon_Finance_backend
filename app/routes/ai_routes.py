from flask import Blueprint, request, jsonify
from app.init_services import ai_service

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/generate_summary', methods=['POST'])
def register():
    data = request.get_json()
    text = data.get('text')
    result = ai_service.generate_summary(text)
    return jsonify(result), 200

