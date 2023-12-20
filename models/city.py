#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class, contains state ID and name
    class attribute __tablename__ : represents the table name, cities
    class attribute name :
        represents a column containing a string (128 characters)
        can't be null
    class attribute state_id:
        represents a column containing a string (60 characters)
        can't be null
        is a foreign key to states.id
    """
    __tablename__ = "cities"
    name = Column("name", String(128), nullable=False)
    state_id = Column(
        "state_id", String(60), ForeignKey("states.id"), nullable=False)
    state = relationship('State', back_populates="cities")
    places = relationship(
        "Place", back_populates="cities", cascade="all, delete, delete-orphan"
        )
