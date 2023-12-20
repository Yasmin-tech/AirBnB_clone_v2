#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    user = relationship("User", back_populates="places")
    cities = relationship("City", back_populates="places")
    reviews = relationship(
            "Review", cascade='all, delete, delete-orphan',
            back_populates="place")
    place_amenity = Table(
            "place_amenity", Base.metadata,
            Column(
                "place_id", String(60), ForeignKey("places.id"),
                primary_key=True, nullable=False),
            Column(
                "amenity_id", String(60), ForeignKey("amenities.id"),
                primary_key=True, nullable=False)
            )
    amenities = relationship(
            "Amenity", secondary="place_amenity", viewonly=False)
    amenity_ids = []

    @property
    def reviews_getter(self):
        """return the list of Review instances with place_id equals
            to the current Place.id.

            Note: this will be a FileStorage relationship between
            Place and Review
        """
        from model.review import Review
        from model import storage

        place_id = self.id
        review_list = []
        for value in storage.all(Review).values():
            if value.place_id == place_id:
                review_list.append(value)
        return review_list

    @property
    def amenities_getter(self):
        """returns the list of Amenity instances based on the attribute
            amenity_ids that contains all Amenity.id linked to the Place
        """
        amenity_list = []
        for value in storage.all(Amentity).values():
            if value.id in self.amenity_ids:
                amenity_list.append(value)
        return amenity_list

    def amenities_s(self, value):
        """Setter attribute amenities that handles append method
            for adding an Amenity.id to the attribute amenity_ids

            Note: This method should accept only Amenity object,
            otherwise, do nothing.
        """
        from models.amenity import Amenity

        if isinstance(value, Amenity):
            self.amenity_ids.append(value.id)
