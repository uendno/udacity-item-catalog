from marshmallow import Schema, fields
from .item import ItemSchema


class CategorySchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    slug = fields.Str(required=True)
    items = fields.Nested(ItemSchema, many=True)


