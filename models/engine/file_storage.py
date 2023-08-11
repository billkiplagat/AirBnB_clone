#!/usr/bin/python3
"""
Module file_storage serializes and
deserializes JSON types
"""
import json
from models.user import User
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        """creates a new object and saves it to __objects"""
        self.__objects[obj.__class__.__name__ + '.' + str(obj.id)] = obj

    def save(self):
        """
        save/serializes obj dictionaries to the JSON file
        (path: __file_path)
        """
        obj_dict = {}
        for key, obj in self.__objects.items():
            obj_dict[key] = obj.to_dict()

        with open(self.__file_path, "w", encoding="UTF-8") as f:
            json.dump(obj_dict, f)
            # f.write("\n")

    def reload(self):
        """
        deserializes the JSON file to __objects, if the JSON
        file exists, otherwise nothing happens
        """
        class_map = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }
        try:
            with open(self.__file_path, 'r') as f:
                dictionary = json.load(f)

                for value in dictionary.values():
                    cls_name = value["__class__"]
                    if cls_name in class_map:
                        cls = class_map[cls_name]
                        self.new(cls(**value))
                    else:
                        pass
        except FileNotFoundError:
            pass
