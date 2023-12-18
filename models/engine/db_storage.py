#!/usr/bin/python3
"""This module contains a class named <DBStorage> which is the
    MYSQL database for all classes
    """

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.city import City
from models.state import State, Base
# from models.place import Place

# from models.base_model import BaseModel

# validClasses = [Place, Amenity, State, City, BaseModel, Review, User]
validClasses = [State, City]


class DBStorage():
    """A DBStorage engine which uses SQLAlchemy ORM to
        interact with MYSQL database
    """
    __engine = None
    __session = None

    def __init__(self):
        """the constructor for DBStorage instances"""
        sql_user = os.environ.get("HBNB_MYSQL_USER")
        sql_pwd = os.environ.get("HBNB_MYSQL_PWD")
        sql_host = os.environ.get("HBNB_MYSQL_HOST")
        sql_db = os.environ.get("HBNB_MYSQL_DB")
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'.format(
                    sql_user, sql_pwd, sql_host, sql_db), pool_pre_ping=True)
        if os.environ.get("HBNB_ENV") == "test":
            Base.metadata.drop_all

    def all(self, cls=None):
        """if cls is not None, return all instances associated with
            with cls otherwise return all instances of all tables
        """
        instances_dict = {}
        if cls in validClasses:
            for each_cls_obj in self.__session.query(cls).all():
                key = "{}.{}".format(
                        each_cls_obj.__class__.__name__, each_cls_obj.id)
                instances_dict[key] = each_cls_obj
            return instances_dict
        all_obj_list = []
        stateObj = self.__session.query(State).all()
        if stateObj:
            all_obj_list.append(stateObj)
        cityObj = self.__session.query(City).all()
        if cityObj:
            all_obj_list.append(cityObj)
        for eachClass in all_obj_list:
            for eachObj in eachClass:
                key = "{}.{}".format(eachObj.__class__.__name__, eachObj.id)
                instances_dict[key] = eachObj
        return instances_dict

    def new(self, obj):
        """add new object to the current database session"""
        self.__session.add(obj)
        self.__session.commit()

    def save(self):
        """commit all changes to the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)
