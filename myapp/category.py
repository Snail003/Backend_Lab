from myapp import app, db
from flask import request
from myapp.models import CategoryModel, UserModel
from myapp.schemas import CategorySchema, CreateCategorySchema

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
create_category_schema = CreateCategorySchema()

@app.post('/category')
def create_category():
    category_data = request.get_json(silent=True)
    if category_data is None:
        return {"error": "No valid JSON data received"}, 400

    try:
        payload = create_category_schema.load(category_data)
    except Exception as e:
        return {"error": str(e)}, 400

    name = payload["name"].strip()
    owner_user_id = payload.get("owner_user_id")
    is_global = owner_user_id is None

    if not is_global:
        owner = UserModel.query.get(owner_user_id)
        if not owner:
            return {"error": "Owner user not found"}, 400

    category = CategoryModel(
        name=name,
        is_global=is_global,
        owner_user_id=None if is_global else owner_user_id
    )
    db.session.add(category)
    db.session.commit()
    return category_schema.dump(category), 201

@app.get('/category')
def get_category():
    user_id = request.args.get("user_id")
    if user_id is None or user_id.strip() == "":
        global_only = CategoryModel.query.filter_by(is_global=True).all()
        return categories_schema.dump(global_only), 200
    user_id = user_id.strip()
    if not user_id.isdigit():
        return {"error": "Invalid user_id"}, 400
    uid = int(user_id)
    items = (
        CategoryModel.query
        .filter(
            (CategoryModel.is_global == True) |
            (CategoryModel.owner_user_id == uid)
        )
        .all()
    )
    return categories_schema.dump(items), 200


@app.delete('/category')
def delete_category():
    category_id = request.args.get("id", "")
    if not category_id or not category_id.strip().isdigit():
        return {"error": "Category could not be found"}, 404

    cid = int(category_id.strip())
    category = CategoryModel.query.get(cid)
    if not category:
        return {"error": "Category could not be found"}, 404

    if not category.is_global:
        owner_user_id = request.args.get("owner_user_id")
        if owner_user_id is None or not owner_user_id.strip().isdigit():
            return {"error": "owner_user_id is required to delete a non-global category"}, 400
        if int(owner_user_id.strip()) != (category.owner_user_id or -1):
            return {"error": "Only the owner can delete this category"}, 403

    db.session.delete(category)
    db.session.commit()
    return category_schema.dump(category), 200