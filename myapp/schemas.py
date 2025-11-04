from marshmallow import Schema, fields, validate, ValidationError, pre_load

_non_empty_str = validate.And(validate.Length(min=1, max=256), lambda s: s.strip() != "")

def _non_negative(value):
    if value < 0:
        raise ValidationError("Must be >= 0.")

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True, validate=_non_empty_str)

class CreateUserSchema(Schema):
    name = fields.String(required=True, validate=_non_empty_str)

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True, validate=_non_empty_str)
    is_global = fields.Boolean(dump_only=True)
    owner_user_id = fields.Int(allow_none=True)

class CreateCategorySchema(Schema):
    name = fields.String(required=True, validate=_non_empty_str)
    owner_user_id = fields.Int(allow_none=True, load_default=None)

class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    creation_time = fields.AwareDateTime(dump_only=True, attribute="created_at")
    expenses = fields.Float(required=True, validate=_non_negative)

    @pre_load
    def normalize(self, data, **kwargs):
        for k, v in list(data.items()):
            if isinstance(v, str):
                data[k] = v.strip()
        if "amount" in data and "expenses" not in data:
            data["expenses"] = data["amount"]
        dt = data.get("creation_time") or data.get("datetime")
        if isinstance(dt, str) and dt.strip().endswith(("Z", "z")):
            data["creation_time"] = dt.strip()[:-1] + "+00:00"
        return data

class CreateRecordSchema(Schema):
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    expenses = fields.Float(required=True, validate=_non_negative)

    @pre_load
    def normalize(self, data, **kwargs):
        for k, v in list(data.items()):
            if isinstance(v, str):
                data[k] = v.strip()
        if "amount" in data and "expenses" not in data:
            data["expenses"] = data["amount"]
        return data
