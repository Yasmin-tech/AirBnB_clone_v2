#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
# from models.state import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String


class Amenity(BaseModel, Base):
    """The class Amenity"""
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship(
            "Place", secondary="place_amenity", back_populates="amenities", viewonly=False)
