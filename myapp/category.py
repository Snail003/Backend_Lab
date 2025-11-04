from myapp import app
from myapp.test_data import categories
from flask import request
import uuid

category_template = {
    "name" : "str"
}

@app.post('/category')
def create_category():
    category_data = request.get_json(silent=True)

    if category_data is None:
        return {
            "error": "No valid JSON data received"
            }, 400
    
    for field in category_template:
        if field not in category_data:
            return {
                "error": "No " + field + " in JSON data"
                }, 400
        elif type(category_data[field]) != type(category_template[field]):
            return {
                "error": "Invalid data type for " + field + " in JSON data"
                }, 400
        elif type(category_data[field]) == str and not category_data[field]:
            return {
                "error": "Empty " + field + " in JSON data"
                }, 400

    category_id = uuid.uuid4().hex
    category = {"id": category_id, "name": category_data["name"]}
    categories[category_id] = category
    return category, 201

@app.get('/category')
def get_category():
    if "id" not in request.args:
        return list(categories.values())

    category_id = request.args.get("id")
    
    if not category_id.strip():
        return list(categories.values())
    
    if category_id not in categories:
        return {
            "error": "Category could not be found"
            }
    
    return categories[category_id]

@app.delete('/category')
def delete_category():
    if "id" not in  request.args:
        return {
            "error": "id argument isn't found"
            }, 404
    
    category_id = request.args.get("id")
    if category_id not in categories:
        return {
            "error": "Category could not be found"
            }
    
    deleted_category = categories[category_id]
    del categories[category_id]
    return deleted_category