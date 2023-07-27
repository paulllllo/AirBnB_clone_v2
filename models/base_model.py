  #!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


class Base:
    """Set charset of all tables."""
    __table_args__ = {
        "mysql_default_charset": "latin1"
    }


Base = declarative_base(cls=Base)


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime(), default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if 'created_at' in kwargs:
                del kwargs['__class__']
                ctd_at = kwargs['created_at']
                kwargs['created_at'] = datetime.strptime(
                        ctd_at, '%Y-%m-%dT%H:%M:%S.%f')
                upd_at = kwargs['updated_at']
                kwargs['updated_at'] = datetime.strptime(
                        upd_at, '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.id = str(uuid.uuid4())
                self.created_at = datetime.now()
                self.updated_at = datetime.now()

            for k in kwargs:
                setattr(self, k, kwargs[k])

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = type(self).__name__
        obj_members = self.__dict__.copy()
        if '_sa_instance_state' in obj_members:
            del obj_members['_sa_instance_state']
        return '[{}] ({}) {}'.format(cls, self.id, obj_members)


    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        if dictionary.get('_sa_instance_state'):
            del dictionary['_sa_instance_state']
        dictionary.update({'__class__': type(self).__name__})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """Delete an instance from storage"""
        from models import storage
        storage.delete(self)
