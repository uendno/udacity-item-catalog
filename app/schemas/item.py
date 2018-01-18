from marshmallow import Schema, fields


class ItemCategorySchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    slug = fields.Str(required=True)


class ItemSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    slug = fields.Str(required=True)
    description = fields.Str(required=True)
    category = fields.Nested(ItemCategorySchema)
    user_id = fields.Int()
