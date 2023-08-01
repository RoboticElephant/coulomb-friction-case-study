from marshmallow import Schema, fields


# class UserSchema(Schema):
#     id = fields.Int(dump_only=True)
#     username = fields.Str(required=True)
#     # Never send password back to client, therefore, `load_only=True`
#     password = fields.Str(required=True, load_only=True)


class PlainFrictionSchema(Schema):
    id = fields.Int(dump_only=True)
    init_velocity = fields.Float()
    coef_friction = fields.Float()
    gravity = fields.Float()


class FrictionSchema(PlainFrictionSchema):
    idx = fields.List(fields.Float())
    velocities = fields.List(fields.Float())
    distances = fields.List(fields.Float())
