#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class Amenity(BaseModel, Base):
    """
    Amenities Class representing amenities a place
    can offer
    """
    __tablename__ = 'amenities'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)

        from models.place import place_amenity
        place_amenities = relationship('Place', backref='amenities',
                                       secondary=place_amenity, viewonly=False)
    else:
        name = ""
