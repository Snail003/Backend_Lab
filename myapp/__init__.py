from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object("myapp.config")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
import myapp.models
import myapp.views
import myapp.user
import myapp.category
import myapp.record