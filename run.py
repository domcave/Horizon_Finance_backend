from flask import g 
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from app import create_app
import os
import importlib.util
from app.models.code_migration import CodeMigration

app = create_app()


CORS(app, supports_credentials=True)


def run_code_migrations():
    """Run any pending migrations."""
    migrations_dir = os.path.join(os.path.dirname(__file__), 'app/code_migrations')
    print(migrations_dir)
    executed_migrations = {m.filename for m in db.session.query(CodeMigration.filename).all()}


@app.before_request
def before_request():
    g.session = sessionmaker(bind=db.engine)()

@app.route('/health', methods=['GET'])
def health_check():
    return 'Healthy', 200


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
