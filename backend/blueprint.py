from flask import Blueprint, request
from flask_jwt_extended import (jwt_optional)
from geoalchemy2.shape import from_shape
from geojson import FeatureCollection
from shapely.geometry import Point
from shapely.geometry import asShape

from gncitizen.utils.utilsjwt import get_id_role_if_exists
from gncitizen.utils.utilssqlalchemy import get_geojson_feature, json_resp
from server import db
from .models import EventModel

blueprint = Blueprint('events', __name__)


#
# @blueprint.route("/")
# def hello():
#     return "Hello World!"

@blueprint.route('/<int:pk>', methods=['GET'])
@json_resp
def get_event(pk):
    """Get an event by id
    ---
    tags:
      - Evènements (Module externe)
    parameters:
      - name: pk
        in: path
        type: integer
        required: true
        example: 1
    definitions:
      properties:
        type: dict
        description: event properties
      geometry:
        type: geojson
        description: GeoJson geometry
    responses:
      200:
        description: A sight detail
    """
    try:
        result = EventModel.query.get(pk)
        result_dict = result.as_dict(True)
        features = []
        feature = get_geojson_feature(result.geom)
        for k in result_dict:
            if k not in ('id_creator', 'geom'):
                feature['properties'][k] = result_dict[k]
            features.append(feature)
        return {'features': features}, 200
    except Exception as e:
        return {'error_message': str(e)}, 400


@blueprint.route('/', methods=['POST'])
@json_resp
@jwt_optional
def post_event():
    """Gestion des évènements
    If method is POST, add a sight to database else, return all sights
        ---
        tags:
          - Evènements (Module externe)
        summary: Creates a new event
        consumes:
          - application/json
        produces:
          - application/json
        parameters:
          - name: body
            in: body
            description: JSON parameters.
            required: true
            schema:
              id: Event
              required:
                - date
                - time
                - organizer
                - geom
                - thematic
                - url
                - contact_email
                - contact_phone
                - picture
              properties:
                date:
                  type: string
                  description: Date
                  required: true
                  example: "2018-09-20"
                time:
                  type: string
                  default:  none
                  example: "20:30"
                organizer:
                  type: string
                  default:  none
                  example: LPO26
                thematic:
                  type: string
                  example: Oiseaux colorés
                url:
                  type: string
                  example: http://example.com/myevent
                contact_email:
                  type: string
                  example: me@domain.tld
                contact_phone:
                  type: string
                  example: +33999999999
                geometry:
                  type: string
                  example: {"type":"Point", "coordinates":[45,5]}
        responses:
          200:
            description: Event created
        """
    try:
        request_datas = dict(request.get_json())

        if request.files:
            file = request.files['file']
            file.save()
        else:
            file = None

        datas2db = {}
        for field in request_datas:
            if hasattr(EventModel, field):
                datas2db[field] = request_datas[field]

        try:
            newevent = EventModel(**datas2db)
        except Exception as e:
            return {'error_message': str(e)}, 400

        try:
            shape = asShape(request_datas['geometry'])
            newevent.geom = from_shape(Point(shape), srid=4326)
        except Exception as e:
            return {'error_message': str(e)}, 400

        newevent.id_creator = get_id_role_if_exists()

        db.session.add(newevent)
        db.session.commit()
        # Réponse en retour
        result = EventModel.query.get(newevent.id_event)
        result_dict = result.as_dict(True)
        features = []
        feature = get_geojson_feature(result.geom)
        for k in result_dict:
            if k not in ('id_creator', 'geom'):
                feature['properties'][k] = result_dict[k]
        features.append(feature)
        return {
                   'message': 'New event created.',
                   'features': features,
               }, 200
    except Exception as e:
        return {'error_message': str(e)}, 400


@blueprint.route('/', methods=['GET'])
@json_resp
def get_events():
    """Get all events
    ---
    tags:
      - Evènements (Module externe)
    definitions:
      FeatureCollection:
        properties:
          type: dict
          description: event properties
        geometry:
          type: geojson
          description: GeoJson geometry
    responses:
      200:
        description: A sight detail
    """
    try:
        events = EventModel.query.all()
        features = []
        for event in events:
            feature = get_geojson_feature(event.geom)
            event_dict = event.as_dict(True)
            for k in event_dict:
                if k not in ('id_creator', 'geom'):
                    feature['properties'][k] = event_dict[k]
                features.append(feature)
        return FeatureCollection(features)
    except Exception as e:
        return {'error_message': str(e)}, 400
