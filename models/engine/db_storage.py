#!/usr/bin/python3

"""This module defines a class to manage db storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.state import State
from models.review import Review
import os


class DBStorage:
    """Database storage class using mysqldb and sqlalchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage module"""
        HBNB_MYSQL_USER = os.environ.get('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = os.environ.get('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = os.environ.get('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = os.environ.get('HBNB_MYSQL_DB')
        HBNB_ENV = os.environ.get('HBNB_ENV')

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_HOST, HBNB_MYSQL_DB),
            pool_pre_ping=True)

        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session for all objects depending
        on the class name (argument: cls)
        """
        models = [User, State, City, Amenity, Place, Review]
        obj_dict = {}

        if cls is None:
            for cls in models:
                for objs in self.__session.query(cls).all():
                    obj = objs.to_dict()
                    key = "{}.{}".format(obj['__class__'], obj['id'])
                    obj_dict[key] = objs
        else:
            for objs in self.__session.query(cls).all():
                obj = objs.to_dict()
                key = "{}.{}".format(obj['__class__'], obj['id'])
                obj_dict[key] = objs
        return obj_dict

    def new(self, obj):
        """Adds new object to the database"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session if not None"""
        models = {
                'State': State,
                'City': City,
                'User': User,
                'Place': Place,
                'Review': Review,
                'Amenity': Amenity}

        self.__session = Session(self.__engine)
        if not obj:
            return
        model = models.get(type(obj).__name__)
        obj = self.__session.query(model).filter(obj.id == model.id).first()
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create Session using sessionmaker"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)

    def close(self):
        """closes the current session"""
        self.__session.remove()
