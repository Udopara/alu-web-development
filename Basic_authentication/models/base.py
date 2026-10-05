#!/usr/bin/env python3
""" Base module for data models
"""
from datetime import datetime
from typing import TypeVar, List, Iterable
import uuid

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


class Base():
    """ Base class for managing object representation and storage
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a Base instance
        """
        s_class = str(self.__class__.__name__)
        if kwargs is not None and len(kwargs) > 0:
            for k, v in kwargs.items():
                if k == 'created_at':
                    self.created_at = datetime.strptime(v, TIMESTAMP_FORMAT)
                elif k == 'updated_at':
                    self.updated_at = datetime.strptime(v, TIMESTAMP_FORMAT)
                elif k != '__class__':
                    setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """ Equality operator for comparing Base instances
        """
        if type(other) is not type(self):
            return False
        if not isinstance(other, Base):
            return False
        return self.id == other.id

    def to_json(self, for_serialization: bool = False) -> dict:
        """ Convert object instance into a JSON dictionary format
        """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key.startswith('_'):
                continue
            if isinstance(value, datetime):
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result

    def save(self):
        """ Save current object state to storage
        """
        self.updated_at = datetime.utcnow()
        from models import DATA
        if self.__class__.__name__ not in DATA:
            DATA[self.__class__.__name__] = {}
        DATA[self.__class__.__name__][self.id] = self
        from models import storage
        storage.save()

    def remove(self):
        """ Remove object from storage
        """
        from models import DATA
        cname = self.__class__.__name__
        if cname in DATA and self.id in DATA[cname]:
            del DATA[cname][self.id]
            from models import storage
            storage.save()
