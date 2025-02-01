from flask import Flask,g 
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from app.config import Config
from app import create_app

app = create_app()

CORS(app, resources={r"/*": {"origins": "*"}})

@app.before_request
def before_request():
    g.session = sessionmaker(bind=db.engine)()

@app.route('/health', methods=['GET'])
def health_check():
    return 'Healthy', 200

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
