#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from models.review import Review
from sqlalchemy.sql.schema import Table

place_amenity = Table("place_amenity", Base.metadata, Column(
        "place_id", String(60), ForeignKey('places.id')), Column(
        "amenity_id", String(60), ForeignKey('amenities.id')),
        mysql_default_charset="latin1"
        )


class Place(BaseModel, Base):
    """Represents the Place table in the db"""
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'))
    user_id = Column(String(60), ForeignKey('users.id'))
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship('Review', backref='place')
    amenity_ids = []   
    amenities = relationship(
            'Amenity',
            secondary='place_amenity',
            viewonly=False)

    @property
    def reviews(self):
        """
        Returns the list of Reviews instances with place_id
        equals to the current place.id
        """
        from models import storage
        objs = []
        for _, value in storage.all(Review).items():
            if self.id == value.place_id:
                objs.append(str(value))
        return objs

    @property
    def amenities(self):
        """
        Returns the list of Amenity instances based on the attribute.
        Amenity_ids that contains all Amenity.id linked to the Place.
        """
        from models import storage
        from models.amenity import Amenity

        objs = []
        for _, value in storage.all(Amenity).items():
            if value.id in self.amenity_ids:
                objs.append(str(value))
        return objs

    @amenities.setter
    def amenities(self, obj):
        """
        Add an Amenity.id to the attribute amenity_ids.
        Only Amenity object, otherwise, do nothing.
        """
        from models.amenity import Amenity

        if type(obj) is not Amenity:
            return
        self.amenity_ids.append(obj.id)
