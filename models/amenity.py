#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from os import getenv


class Amenity(BaseModel, Base):
    """
    Amenities Class representing amenities a place
    can offer
    """
    __tablename__ = 'amenities'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)

        place_amenity = Table('place_amenity', Base.metadata,
                              Column('place_id', String(60),
                                     ForeignKey('places.id'), primary_key=True),
                              Column('amenity_id', String(60),
                                     ForeignKey('amenities.id'), primary_key=True))
    else:
        name = ""
