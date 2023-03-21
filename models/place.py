#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'), primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'), primary_key=True))

    '''amenities for DBStorage'''
    amenities = relationship('Amenity', backref='places',
                             secondary=place_amenity, viewonly=False)

    '''amenities for FileStorage'''
    @property
    def amenities(self):
        '''
        returns the list of Amenity instances based on the attribute
        amenity_ids that contains all Amenity.id linked to the Place
        '''
        from os import getenv
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            from models import storage
            from models.amenity import Amenity
            result = storage.all(Amenity)
            return [amenity_obj for amenity_obj in result.values()
                    if amenity_obj.id in self.amenity_ids]

    @amenities.setter
    def amenities(self, amenity):
        """
        Setter attribute amenities that handles append method for adding an
        Amenity.id to the attribute amenity_ids. This method should accept only
        Amenity object, otherwise, do nothing.
        """

        if type(amenity).__name__ == 'Amenity':
            self.amenity_ids.append(amenity.id)

    '''reviews for DBStorage'''
    reviews = relationship('Review', backref='place',
                           cascade='all, delete, delete-orphan')

    '''reviews for FileStorage'''
    @property
    def reviews(self):
        '''
        returns the list of Review instances
        with place_id equals to the current Place.id => It will be the
        FileStorage relationship between Place and Review
        '''
        from os import getenv
        if getenv('HBNB_TYPE_STORAGE') != 'db':
            from models import storage
            from models.review import Review
            result = storage.all(Review)
            return [review_obj for review_obj in result.values()
                    if self.id == review_obj.place_id]
