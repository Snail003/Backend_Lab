from flask import request
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from myapp import app, db
from myapp.models import UserModel
from myapp.schemas import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.post('/user')
def create_user():
    user_data = request.get_json(silent=True) or {}
    username = (user_data.get("username") or "").strip()
    password = (user_data.get("password") or "").strip()
    if not username or not password:
        return {"error": "username and password are required"}, 400
    if UserModel.query.filter_by(name=username).first():
        return {"error": "User with this username already exists"}, 400
    user = UserModel(
        name=username,
        password=pbkdf2_sha256.hash(user_data["password"]),
    )
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201


@app.post('/login')
def login():
    user_data = request.get_json(silent=True) or {}
    username = (user_data.get("username") or "").strip()
    password = (user_data.get("password") or "").strip()
    if not username or not password:
        return {"error": "username and password are required"}, 400
    user = UserModel.query.filter_by(name=username).first()
    if user and pbkdf2_sha256.verify(user_data["password"], user.password):
        access_token = create_access_token(identity=str(user.id))
        return {"access_token": access_token}, 200
    return {"error": "Invalid username or password"}, 401


@app.get('/user/<int:user_id>')
@jwt_required()
def get_user(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return {"error": "User could not be found"}, 404
    return user_schema.dump(user)


@app.delete('/user/<int:user_id>')
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return {"error": "Only the owner can delete this user"}, 403
    user = UserModel.query.get(user_id)
    if not user:
        return {"error": "User could not be found"}, 404
    db.session.delete(user)
    db.session.commit()
    return user_schema.dump(user)


@app.get('/users')
@jwt_required()
def get_users():
    all_users = UserModel.query.all()
    return users_schema.dump(all_users)

