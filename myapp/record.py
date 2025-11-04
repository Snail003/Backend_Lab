from myapp import app, db
from flask import request
from datetime import datetime, timezone
from myapp.models import RecordModel, UserModel, CategoryModel
from myapp.schemas import RecordSchema

record_schema = RecordSchema()
records_schema = RecordSchema(many=True)
@app.post('/record')
def create_record():
    record_data = request.get_json(silent=True)
    if record_data is None:
        return {"error": "No valid JSON data received"}, 400

    try:
        payload = record_schema.load(record_data)
    except Exception as e:
        return {"error": str(e)}, 400

    user_id = payload["user_id"]
    category_id = payload["category_id"]
    expenses = payload["amount"] if "amount" in payload else payload.get("expenses", None)
    if expenses is None:
        expenses = payload.get("expenses")
    try:
        expenses = float(expenses)
    except Exception:
        return {"error": "Invalid data type for expenses in JSON data"}, 400
    if expenses < 0:
        return {"error": "expenses can't be negative"}, 400

    user = UserModel.query.get(user_id)
    if not user:
        return {"error": "User could not be found"}, 404
    category = CategoryModel.query.get(category_id)
    if not category:
        return {"error": "Category could not be found"}, 404

    is_global = getattr(category, "is_global", False)
    owner_user_id = getattr(category, "owner_user_id", None)
    if not is_global and owner_user_id is not None and owner_user_id != user.id:
        return {"error": "Category belongs to another user"}, 403

    rec = RecordModel(
        user_id=user.id,
        category_id=category.id,
        expenses=expenses,
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(rec)
    db.session.commit()
    return record_schema.dump(rec), 201

@app.get('/record/<record_id>')
def get_record(record_id):
    try:
        rid = int(record_id)
    except ValueError:
        return {"error": "Record could not be found"}, 404

    rec = RecordModel.query.get(rid)
    if not rec:
        return {"error": "Record could not be found"}, 404
    return record_schema.dump(rec)

@app.delete('/record/<record_id>')
def delete_record(record_id):
    try:
        rid = int(record_id)
    except ValueError:
        return {"error": "Record could not be found"}, 404

    rec = RecordModel.query.get(rid)
    if not rec:
        return {"error": "Record could not be found"}, 404

    db.session.delete(rec)
    db.session.commit()
    return record_schema.dump(rec)

@app.get('/record')
def get_sorted_records():
    use_user_id = True
    use_category_id = True

    if "user_id" not in request.args:
        use_user_id = False
    if "category_id" not in request.args:
        use_category_id = False
    if not use_category_id and not use_user_id:
        return {"error": "No valid arguments were found"}, 404

    user_id = request.args.get("user_id", "")
    category_id = request.args.get("category_id", "")

    if not user_id.strip() and not category_id.strip():
        all_records = RecordModel.query.all()
        return records_schema.dump(all_records)

    q = RecordModel.query

    if use_user_id and user_id.strip():
        if not user_id.isdigit():
            return {"error": "User could not be found"}, 404
        q = q.filter(RecordModel.user_id == int(user_id))

    if use_category_id and category_id.strip():
        if not category_id.isdigit():
            return {"error": "Category could not be found"}, 404
        q = q.filter(RecordModel.category_id == int(category_id))

    result = q.all()
    return records_schema.dump(result)
