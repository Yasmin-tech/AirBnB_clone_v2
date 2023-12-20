#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This class defines a user by various attributes

    User inherits from BaseModel and Base (respect the order)
    class attribute:  __tablename__ represents the table name, users
                    email: represents a column containing a string
                        (128 characters)
                        can't be null
                    password: represents a column containing a string
                        (128 characters)
                        can't be null

                    first_name: represents a column containing a string
                        (128 characters)
                        can be null
                    last_name: represents a column containing a string
                    (128 characters)
                    can be null
    """
    # email = ''
    # password = ''
    # first_name = ''
    # last_name = ''

    __tablename__ = "users"

    email = Column("email", String(128), nullable=False)
    password = Column("password", String(128), nullable=False)
    first_name = Column("first_name", String(128), nullable=True)
    last_name = Column("last_name", String(128), nullable=True)

    places = relationship(
        "Place", back_populates="user", cascade="all, delete, delete-orphan")
    reviews = relationship(
        "Review", back_populates="user", cascade="all, delete, delete-orphan")
