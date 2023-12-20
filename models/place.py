#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay
    """
    # city_id = ""
    # user_id = ""
    # name = ""
    # description = ""
    # number_rooms = 0
    # number_bathrooms = 0
    # max_guest = 0
    # price_by_night = 0
    # latitude = 0.0
    # longitude = 0.0
    # amenity_ids = []

    __tablename__ = "places"

    city_id = Column(
        "city_id", String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(
        "user_id", String(60), ForeignKey("users.id"), nullable=False)
    name = Column("name", String(128), nullable=False)
    description = Column("description", String(1024), nullable=True)
    number_rooms = Column("number_rooms", Integer, nullable=False, default=0)
    max_guest = Column("max_guest", Integer, nullable=False, default=0)
    price_by_night = Column(
        "price_by_night", Integer, nullable=False, default=0)
    latitude = Column("latitude", Float, nullable=True)
    longitude = Column("longitude", Float, nullable=True)

    user = relationship("User", back_populates="places")
    cities = relationship("City", back_populates="places")
    reviews = relationship(
        "Review", back_populates="place",
        cascade="all, delete, delete-orphan")

    @property
    def reviews_attr(self):
        """  returns the list of Review instances with place_id
        equals to the current Place.id"""
        from models import storage
        from models.review import Review

        list_reviews = []
        reviews_objs = storage.all(Review)

        for key, obj in reviews_objs.items():
            if obj.place_id == self.id:
                list_reviews.append(obj)

        return list_reviews
