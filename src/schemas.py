from marshmallow import Schema, fields

class ItemsSchema(Schema):
    id = fields.Str(dump_only=True) # this is not received and only returned in the response
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(dump_only=True)

class GetItemsSchema(Schema):
    items = fields.List(fields.Nested(ItemsSchema))

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class StoreUpdateSchema(Schema):
    name = fields.Str(required=True)