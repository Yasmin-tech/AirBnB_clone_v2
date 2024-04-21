#!/usr/bin/python3
""" This module defines a class to manage database storage for hbnb clone"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

validClasses = [State, City, User, Place, Review, Amenity]


class DBStorage():
    """
    Private class attributes:
            __engine: set to None
            __session: set to None

    Public instance methods:
        __init__(self):
            create the engine (self.__engine) ->
            linke the __engine to the MySQL database
            dialect: mysql
            driver: mysqldb

            all of the following values must be retrieved
            via environment variables:
                MySQL user: HBNB_MYSQL_USER
                MySQL password: HBNB_MYSQL_PWD
                MySQL host: HBNB_MYSQL_HOST (here = localhost)
                MySQL database: HBNB_MYSQL_DB
                the option pool_pre_ping=True
                drop all tables if the environment variable
                HBNB_ENV is equal to test
    """

    __engine = None
    __session = None

    def __init__(self) -> None:
        """
        create db storage:
            create the engine (self.__engine) ->
            linke the __engine to the MySQL database
            dialect: mysql
            driver: mysqldb

            all of the following values must be retrieved
            via environment variables:
                MySQL user: HBNB_MYSQL_USER
                MySQL password: HBNB_MYSQL_PWD
                MySQL host: HBNB_MYSQL_HOST (here = localhost)
                MySQL database: HBNB_MYSQL_DB
                the option pool_pre_ping=True
                drop all tables if the environment variable
                HBNB_ENV is equal to test
        """
        sql_user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db_name = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            sql_user, passwd, host, db_name), pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """ create all tables in the database
            create the current database session (self.__session)
                 from the engine (self.__engine
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def new(self, obj):
        """ A method to add the object to the current database session
        (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """  commit all changes of the current database session
        (self.__session)"""
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def all(self, cls=None):
        """ query on the current database session (self.__session)
        all objects depending of the class name (argument cls)
        if cls=None, query all types of objects
            (User, State, City, Amenity, Place and Review)
        return a dictionary: ->key = <class-name>.<object-id>
                               value = object """
        objs_dict = {}
        if cls and cls in validClasses:
            for obj in self.__session.query(cls).all():
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                objs_dict[key] = obj
        else:
            for class_ in Base.registry._class_registry.values():
                if hasattr(class_, '__table__'):
                    for obj in self.__session.query(class_).all():
                        key = "{}.{}".format(obj.__class__.__name__, obj.id)
                        objs_dict[key] = obj
        return (objs_dict)

    def close(self):
        """ remove the session
        """
        self.__session.remove()
