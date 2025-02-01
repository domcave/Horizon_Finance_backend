from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token
from datetime import timedelta

def register_user(username, email, password, first_name, last_name):
    if db.session.query(User).filter_by(email=email).first():
        return {"error": "Email already registered"}, 400

    new_user = User(username=username, email=email, first_name=first_name, last_name=last_name)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201

def login_user(email, password):
    user = db.session.query(User).filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return {"error": "Invalid email or password"}, 401

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
    
    return {"access_token": access_token}, 200
