from flask import request
from myapp import app, db
from myapp.models import UserModel
from myapp.schemas import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.post('/user')
def create_user():
    user_data = request.get_json(silent=True) or {}
    username = (user_data.get("username") or "").strip()
    if not username:
        return {"error": "Empty username in JSON data"}, 400

    user = UserModel(name=username)
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201

@app.get('/user/<int:user_id>')
def get_user(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return {"error": "User could not be found"}, 404
    return user_schema.dump(user)

@app.delete('/user/<int:user_id>')
def delete_user(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return {"error": "User could not be found"}, 404
    db.session.delete(user)
    db.session.commit()
    return user_schema.dump(user)

@app.get('/users')
def get_users():
    all_users = UserModel.query.all()
    return users_schema.dump(all_users), 201

