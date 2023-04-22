#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from models import storage
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False)
    cur_date = datetime.utcnow()
    created_at = Column(DateTime, nullable=False, default=cur_date)
    updated_at = Column(DateTime, nullable=False, default=cur_date)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.now()
        if kwargs:
            for k, v in kwargs.items():
                if k == 'created_at' or k == 'updated_at':
                    v = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f")
                if k != "__class__":
                    setattr(self, k, v)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        object_dict = self.__dict__.copy()
        if object_dict.get('_sa_instance_state'):
            del object_dict['_sa_instance_state']
        return '[{}] ({}) {}'.format(cls, self.id, object_dict)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def delete(self):
        """delete the current instance from the storage (models.storage)"""
        storage.delete(self)

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__.copy())
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if dictionary.get('_sa_instance_state'):
            del dictionary['_sa_instance_state']
        return dictionary


def dict_convert_no_value(kwargs):
    for key, value in kwargs.items():
        if key not in ['city_id', 'user_id', 'created_at', 'updated_at']\
                and type(value) not in [int, float, datetime]:
            if value.isnumeric():
                kwargs[key] = int(value)
            elif isfloat(value):
                kwargs[key] = float(value)

    return kwargs


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
