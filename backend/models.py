#!/usr/bin/python3
# -*- coding: utf-8 -*-

from geoalchemy2 import Geometry

from gncitizen.core.ref_geo.models import LAreas
from gncitizen.core.commons.models import TimestampMixinModel
from gncitizen.core.users.models import UserModel
from gncitizen.utils.utilssqlalchemy import serializable, geoserializable
from server import db


def create_schema(db):
    db.session.execute('CREATE SCHEMA IF NOT EXISTS gnc_events')
    db.session.commit()


@serializable
@geoserializable
class EventModel(TimestampMixinModel, db.Model):
    """Table des évènements"""
    __tablename__ = 't_events'
    __table_args__ = {'schema': 'gnc_events'}
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
    municipality = db.Column(db.Integer, db.ForeignKey(LAreas.id_area))
    id_creator = db.Column(db.Integer, db.ForeignKey(UserModel.id_user))
