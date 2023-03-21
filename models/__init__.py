#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import getenv

__all__ = ["amenity", "base_model", "city", "place", "review", "state", "user"]

storage = None
if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
