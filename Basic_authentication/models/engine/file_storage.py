#!/usr/bin/env python3
""" FileStorage module for JSON file persistence
"""
import json
import os
from typing import TypeVar, List, Dict


class FileStorage():
    """ FileStorage class managing object serialization and deserialization
    """
    __file_path = "db.json"
    __objects = {}

    def __init__(self):
        """ Initialize FileStorage instance
        """
        self.reload()

    def all(self, cls=None) -> Dict[str, TypeVar('Base')]:
        """ Return dictionary of stored objects
        """
        if cls is None:
            return self.__objects
        if isinstance(cls, str):
            return self.__objects.get(cls, {})
        return self.__objects.get(cls.__name__, {})

    def new(self, obj: TypeVar('Base')):
        """ Add object to __objects mapping
        """
        if obj is not None:
            key = obj.__class__.__name__
            if key not in self.__objects:
                self.__objects[key] = {}
            self.__objects[key][obj.id] = obj

    def save(self):
        """ Serialize __objects to the JSON file
        """
        json_objects = {}
        for class_name, objects in self.__objects.items():
            json_objects[class_name] = {}
            for obj_id, obj in objects.items():
                json_objects[class_name][obj_id] = obj.to_json(True)

        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """ Deserialize JSON file data into __objects
        """
        if not os.path.exists(self.__file_path):
            return

        with open(self.__file_path, 'r') as f:
            try:
                json_objects = json.load(f)
            except Exception:
                return

        from models.user import User
        classes = {"User": User}

        for class_name, objects in json_objects.items():
            if class_name in classes:
                cls = classes[class_name]
                self.__objects[class_name] = {}
                for obj_id, obj_dict in objects.items():
                    self.__objects[class_name][obj_id] = cls(**obj_dict)

    def count(self, cls=None) -> int:
        """ Count total stored objects for a class
        """
        if cls is None:
            total = 0
            for objects in self.__objects.values():
                total += len(objects)
            return total
        return len(self.all(cls))

    def get(self, cls, id: str) -> TypeVar('Base'):
        """ Retrieve object by class and ID
        """
        if cls is None or id is None:
            return None
        return self.all(cls).get(id)

    def search(self, cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """ Search objects matching given attributes dictionary
        """
        result = []
        if cls is None:
            return result
        all_objs = self.all(cls)
        for obj in all_objs.values():
            match = True
            for key, value in attributes.items():
                if not hasattr(obj, key) or getattr(obj, key) != value:
                    match = False
                    break
            if match:
                result.append(obj)
        return result
