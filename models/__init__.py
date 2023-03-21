#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""


from os import getenv

storage = None
if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()

"""support for lines like `from models import *`
"""
if True:
    from models.state import State
    from models.city import City
    from models.user import User
