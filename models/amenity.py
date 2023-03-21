#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String


class Amenity(BaseModel):
    """
    Amenities Class representing amenities a place
    can offer
    """
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)
