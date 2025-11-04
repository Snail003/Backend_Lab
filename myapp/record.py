from myapp import app
from myapp.test_data import records
from flask import request
from datetime import datetime
import uuid

record_template = {
    "user_id" : "str",
    "category_id" : "str",
    "expenses" : 0,
}

@app.post('/record')
def create_record():
    record_data = request.get_json(silent=True)

    if record_data is None:
        return {
            "error": "No valid JSON data received"
            }, 400
    
    for field in record_template:
        if field not in record_data:
            return {
                "error": "No " + field + " in JSON data"
                }, 400
        elif type(record_data[field]) != type(record_template[field]):
            return {
                "error": "Invalid data type for " + field + " in JSON data"
                }, 400
        elif type(record_data[field]) == str and not record_data[field]:
            return {
                "error": "Empty " + field + " in JSON data"
                }, 400
        elif type(record_data[field]) == int and record_data[field] < 0:
            return {
                "error": field + " can't be negative"
                }, 400

    record_id = uuid.uuid4().hex
    record = {"id": record_id}
    record["user_id"] = record_data["user_id"]
    record["category_id"] = record_data["category_id"]
    record["creation_time"] = datetime.now()
    record["expenses"] = record_data["expenses"]
    records[record_id] = record
    return record, 201

@app.get('/record/<record_id>')
def get_record(record_id):
    if record_id not in records:
        return {
            "error": "Record could not be found"
            }, 404
    
    return records[record_id]

@app.delete('/record/<record_id>')
def delete_record(record_id):
    if record_id not in records:
        return {
            "error": "Record could not be found"
            }, 404
    
    deleted_record = records[record_id]
    del records[record_id]
    return deleted_record

@app.get('/record')
def get_sorted_records():
    use_user_id = True
    use_category_id = True

    if "user_id" not in request.args:
        use_user_id = False
    if "category_id" not in request.args:
        use_category_id = False
    if not use_category_id and not use_user_id:
        return {
            "error": "No valid arguments were found"
            }, 404

    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")

    if not user_id.strip() and not category_id.strip():
        return list(records.values())
    
    response = []

    for key in records:
        if use_category_id and use_user_id:
            if records[key]["user_id"] == user_id and records[key]["category_id"] == category_id:
                response.append(records[key])
            elif use_category_id and records[key]["category_id"] == category_id:
                response.append(records[key])
            elif use_user_id and records[key]["user_id"] == user_id:
                response.append(records[key])

    return response