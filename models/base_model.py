#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime


def dict_convert_no_value(kwargs):
    for key, value in kwargs.items():
        if key not in ['city_id', 'user_id', 'created_at', 'updated_at']:
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


class BaseModel:
    """A base class for all hbnb models"""

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        from models import storage
        new = None
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            if kwargs.get('updated_at') is not None:
                kwargs['updated_at'] =\
                    datetime.strptime(
                        kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.updated_at = datetime.now()
            if kwargs.get('created_at') is not None:
                kwargs['created_at'] =\
                    datetime.strptime(kwargs['created_at'],
                                      '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.created_at = datetime.now()
            if kwargs.get('__class__') is not None:
                del kwargs['__class__']

            if kwargs.get('id') is None:
                self.id = str(uuid.uuid4())
                new = True

            kwargs = dict_convert_no_value(kwargs)
            self.__dict__.update(kwargs)

            if new is not None:
                storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
