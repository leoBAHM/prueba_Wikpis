from marshmallow import fields

from API.extensions import mars


class PersonsSchema(mars.Schema):
    id = fields.Integer(dump_only=True)
    id_person = fields.String()
    name = fields.String()
    last_name = fields.String()

class StudiesSchema(mars.Schema):
    id = fields.Integer(dump_only=True)
    study = fields.String()