#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', cascade='all, delete, delete-orphan',
                          backref='state')

    if os.environ.get('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """Return the list of cities whose state_id equal to state.id"""
            from models import storage

            dict_city = storage.all(City)
            output = []

            for key in dict_city:
                city = dict_city[key]
                if self.id == city.state_id:
                    output.append(city)
            return output
