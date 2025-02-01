from flask import g 
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from app import create_app
import os
import importlib.util
from app.models.code_migration import CodeMigration

app = create_app()

CORS(app, resources={r"/*": {"origins": "*"}})

def run_code_migrations():
    """Run any pending migrations."""
    migrations_dir = os.path.join(os.path.dirname(__file__), 'app/code_migrations')
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
                migration_module.run(db)

                migration_record = CodeMigration(filename=filename)
                db.session.add(migration_record)
                db.session.commit()
            else:
                print(f"Migration {filename} does not have a run() method. Skipping...")

@app.before_request
def before_request():
    g.session = sessionmaker(bind=db.engine)()

@app.route('/health', methods=['GET'])
def health_check():
    return 'Healthy', 200

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
