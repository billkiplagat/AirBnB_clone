#!/usr/bin/python3
"""
Module file_storage serializes and
deserializes JSON types
"""
import json
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        """Sets new objects to existing dictionary of instances saved in __objects"""
        self.__objects[obj.__class__.__name__ + '.' + str(obj.id)] = obj  # we should use obj.id not str(obj) only

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

    def reload(self):
        """
        deserializes the JSON file to __objects, if the JSON
        file exists, otherwise nothing happens
        """
        class_map = {
            "BaseModel": BaseModel
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
