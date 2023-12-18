#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
import models
from sqlalchemy.orm import relationship

Base = declarative_base()


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship(
            "City", back_populates="state",
            cascade="all, delete, delete-orphan")

    @property
    def cities_getter(self):
        """a getter to return the list of associated cities.
            It will be the FileStorage relationship between
            State and City
        """
        state_id = self.id
        city_list = []
        for value in models.storage.all(models.city.City).values():
            if value.state_id == state_id:
                city_list.append(value)
        return city_list
    # name = ""
