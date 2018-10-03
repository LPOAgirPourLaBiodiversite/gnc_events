from geoalchemy2 import Geometry

from gncitizen.utils.utilssqlalchemy import serializable, geoserializable
from server import db
from datetime import datetime


@serializable
@geoserializable
class EventModel(db.Model):
    """Table des observations"""
    __tablename__ = 'events'
    __table_args__ = {'schema': 'gncitizen'}
    id_event = db.Column(db.Integer, primary_key=True, unique=True)
    organizer = db.Column(db.String(200))
    thematic = db.Column(db.String(200))
    description = db.Column(db.String(300))
    date = db.Column(db.DATE, nullable=False)
    time = db.Column(db.TIME)
    url = db.Column(db.String(150))
    contact_email = db.Column(db.String(150))
    contact_phone = db.Column(db.String(150))
    picture = db.Column(db.Text)
    geom = db.Column(Geometry('POINT', 4326))
    municipality = db.Column(db.String(5), db.ForeignKey('ref_geo.li_municipalities.id_municipality'))
    id_creator = db.Column(db.Integer, db.ForeignKey('gncitizen.users.id_user'))
    timestamp_create = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
