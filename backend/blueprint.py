from flask import Blueprint, request, jsonify
from geoalchemy2.shape import from_shape
from marshmallow import ValidationError
from shapely.geometry import Point

from gncitizen.utils.utilssqlalchemy import get_geojson_feature, json_resp
from server import db
from .models import EventModel
from .schemas import event_schema
from datetime import datetime
from datetime import date
blueprint = Blueprint('events', __name__)


#
# @blueprint.route("/")
# def hello():
#     return "Hello World!"

@blueprint.route('/', methods=['GET'])
@json_resp
def get_events():
    """
    List all events
    ---
    tags:
      - Evènements (Module externe)
    responses:
      200:
        description: A list of all sights
    """
    events = EventModel.query.all()
    return events


@blueprint.route('/', methods=['POST'])
# @jwt_optional
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
                  type: date
                  description: Date
                  format: date
                  example: 2018-09-15
                time:
                  type: string
                  default:  none
                  example: 18:00
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
                geom:
                  type: string
                  example: {"type":"Point", "coordinates":[45,5]}
        responses:
          200:
            description: Event created
        """
    json_data = request.get_json()
    medias = request.files
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    # info: manque la date
    try:
        data, errors = event_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    try:
        # Trouver le moyen d'intégrer le datetime
        date = date(datetime.now())
    except:
        return jsonify('Date incomplète'), 422
    try:
        organizer = data['organizer']
    except:
        return jsonify('organizer incomplète'), 422
    try:
        geom = from_shape(Point(data['geom']['coordinates']), srid=4326)
    except:
        return jsonify('geom incomplète'), 422
    try:
        thematic = data['thematic']
    except:
        return jsonify('thematic incomplète'), 422
    try:
        description = data['description']
    except:
        return jsonify('description incomplète'), 422
    try:
        time = data['time']
    except:
        return jsonify('description incomplète'), 422
    url = data['url']
    contact_email = data['contact_email']
    contact_phone = data['contact_phone']
    picture = data['picture']
    # try:
    #     query = LiMunicipalities.query.join(LAreas, LAreas.ip_area == LiMunicipalities.id_area).add_columns(LiMunicipalities.nom_com).first()
    #     print(query)
    #     # municipality = db.session.query(query).filter(func.ST_Intersects(query.geom, geom))
    # except:
    #     return jsonify('impossible de trouver la commune'), 422

    # Si l'utilisateur est connecté, attribut ajoute l'id_role de l'utilisateur.
    # Sinon, complète le champ obs_txt.
    # Si obs_txt est vice, indique 'Anonyme'

    # Create new sight
    event = EventModel(
        date=date,
        organizer=organizer,
        geom=geom,
        thematic=thematic,
        description=description,
        time=time,
        url=url,
        contact_email=contact_email,
        contact_phone=contact_phone,
        picture=picture
    )

    db.session.add(event)
    db.session.commit()
    # Réponse en retour
    result = EventModel.query.get(event.id_event)
    features = []
    feature = get_geojson_feature(result.geom)
    feature['properties'] = result.as_dict(True)
    features.append(feature)
    return jsonify({
        'message': 'New sight created.',
        'features': features,
    }), 200
