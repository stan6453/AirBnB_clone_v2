#!/usr/bin/python3
"""Database storage engine for Airbnb project"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv

from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.place import place_amenity


class DBStorage():
    """Database storage engine class for Airbnb project"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the Database storage"""
        user = getenv('HBNB_MYSQL_USER', 'hbnb_dev')
        password = getenv('HBNB_MYSQL_PWD', 'hbnb_dev_pwd')
        host = getenv('HBNB_MYSQL_HOST', 'localhost')
        database = getenv('HBNB_MYSQL_DB', 'hbnb_dev_db')

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'
            .format(user, password, host, database),
            pool_pre_ping=True
        )

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """query on the current database session (self.__session) all objects
        depending of the class name (argument cls)"""
        result_dict = {}
        for model in [User, State, City, Place, Amenity, Review]:
            if cls is not None and model != cls:
                continue
            query_results = self.__session.query(model).all()
            for obj in query_results:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                result_dict[key] = obj
        return result_dict

    def new(self, obj):
        """add the object to the current database session"""
        if obj:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception:
                self.__session.rollback()

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        1) Create all tables in the database,
        2) creates a new session for database access
        """
        Base.metadata.create_all(bind=self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        call remove() method on the private session attribute (self.__session)
        or close() on the class Session
        """
        self.__session.close()
