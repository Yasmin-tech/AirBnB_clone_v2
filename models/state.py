#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class
    class attribute __tablename__: represents the table name, states
    class attribute name:
        represents a column containing a string (128 characters)
        can't be null
    for DBStorage: class attribute cities:
        represent a relationship with the class City.
        If the State object is deleted,
        all linked City objects must be automatically deleted.
        Also, the reference from a City object to his State should be named
        state
    for FileStorage: getter attribute cities that returns the list of City
    instances with state_id equals to the current
    State.id => It will be the FileStorage relationship between State and City
    """
    __tablename__ = "states"
    name = Column("name", String(128), nullable=False)
    # cities = relationship("City", backref="state",
    # cascade="all, delete, delete-orphan")
    cities = relationship(
        'City', back_populates="state", cascade="all, delete, delete-orphan")

    @property
    def cities_attr(self):
        from models import storage
        from models.city import City
        cities_objs = storage.all(City)
        list_cities = []

        for key, value in cities_objs.items():
            if self.id == value.state_id:
                list_cities.append(value)

        return list_cities
