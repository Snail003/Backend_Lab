from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os
app = Flask(__name__)
app.config.from_object("myapp.config")

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

import myapp.models
import myapp.views
import myapp.user
import myapp.category
import myapp.record
import myapp.test_data


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )