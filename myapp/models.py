from sqlalchemy import func
from myapp import db

class UserModel(db.Model):
    __tablename__ = "user"
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    record = db.relationship("RecordModel", back_populates="user", lazy="dynamic")

class CategoryModel(db.Model):
    __tablename__ = "category"
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(128), unique=False, nullable=False)
    is_global     = db.Column(db.Boolean, default=False, nullable=False)
    owner_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    record = db.relationship("RecordModel", back_populates="category", lazy="dynamic")

class RecordModel(db.Model):
    __tablename__ = "record"
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey("user.id"),    nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    created_at  = db.Column(db.TIMESTAMP, server_default=func.now())
    expenses    = db.Column(db.Float(precision=2), nullable=False)

    user     = db.relationship("UserModel",     back_populates="record")
    category = db.relationship("CategoryModel", back_populates="record")