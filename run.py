from flask import g 
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from app import create_app
import os
from app.models.code_migration import CodeMigration

app = create_app()


CORS(app, supports_credentials=True)

@app.before_request
def before_request():
    g.session = sessionmaker(bind=db.engine)()

@app.route('/health', methods=['GET'])
def health_check():
    return 'Healthy', 200


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
else:
    gunicorn_app = create_app()
