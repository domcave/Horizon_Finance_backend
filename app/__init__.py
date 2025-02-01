from flask import Flask
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
from app.extensions import db, jwt, bcrypt
import importlib.util
from app.models.code_migration import CodeMigration



def run_code_migrations():
    """Run any pending migrations."""
    migrations_dir = os.path.join(os.path.dirname(__file__), 'code_migrations')
    print(migrations_dir)
    executed_migrations = {m.filename for m in db.session.query(CodeMigration.filename).all()}

    for filename in sorted(os.listdir(migrations_dir)):
        if filename.endswith('.py') and filename not in executed_migrations:
            filepath = os.path.join(migrations_dir, filename)
            
            spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
            migration_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(migration_module)
            
            if hasattr(migration_module, 'run'):
                print(f"Executing migration: {filename}")
                migration_module.run()

                migration_record = CodeMigration(filename=filename)
                db.session.add(migration_record)
                db.session.commit()
            else:
                print(f"Migration {filename} does not have a run() method. Skipping...")
                
def initialize_migrations():
    print("Checking Code Migrations...")

    db.create_all()
    run_code_migrations()

def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwtsecretkey')
    app.config['CORS_HEADERS'] = 'Content-Type'

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.routes.plaid_routes import plaid_bp
    app.register_blueprint(plaid_bp, url_prefix="/plaid")

    from app.routes.ai_routes import ai_bp
    app.register_blueprint(ai_bp, url_prefix='/ai')

    with app.app_context():
        initialize_migrations()

    return app
