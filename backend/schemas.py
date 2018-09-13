# from geoalchemy2.shape import to_shape
# from geojson import GeometryCollection
# from marshmallow import pre_dump
from marshmallow import Schema, fields

from gncitizen.utils.utilspost import must_not_be_blank


# class SpecieSchema(Schema):
#     """Schéma Marschmallow des espèces"""
#     id = fields.Int()
#     cd_nom = fields.Int()
#     common_name = fields.Str()
#     sci_name = fields.Str()
#
#     def format_name(self, specie):
#         return '{}, (<i>{}</i>)'.format(specie.common_name, specie.sci_name)


class EventSchema(Schema):
    """Schéma marshmallow des évènements"""
    id_event = fields.Integer(dump_only=True)
    organizer = fields.String(required=True)
    thematic = fields.String(required=True)
    description = fields.String(required=False)
    date = fields.Date(required=True)
    time = fields.Time(required=False)
    url = fields.URL(required=False)
    contact_email = fields.Email(required=False)
    contact_phone = fields.String(required=False)
    picture = fields.String(required=False)
    geom = fields.Dict(required=True, validate=[must_not_be_blank])
    municipality = fields.String(required=False)
    timestamp_create = fields.DateTime(dump_only=True)

    # @pre_dump(pass_many=False)
    # def wkb_to_geojson(self, data):
    #     data.geom = GeometryCollection(to_shape(data.geom))
    #     return data


event_schema = EventSchema()
events_schema = EventSchema(many=True)
