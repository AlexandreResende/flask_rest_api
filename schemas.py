from marshmallow import Schema, fields

class ItemsFields(Schema):
    id = fields.Str(dump_only=True) # this is not received and only returned in the response
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(dump_only=True)

class ItemUpdate(Schema):
    name = fields.Str()
    price = fields.Float()

class StoreFIelds(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)