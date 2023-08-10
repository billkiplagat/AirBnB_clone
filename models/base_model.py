#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    def __init__(self, *args, **kwargs):
        """Public instance attributes initialization
        after creation
        Args:
        *args(args): arguments
        **kwargs(dict): attribute values
        """
        date_format = '%Y-%m-%dT%H:%M:%S.%f'
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
        else:
            for key, value in kwargs.items():
                if key in ("updated_at", "created_at"):
                    self.__dict__[key] = datetime.strptime(value, date_format)
                elif key[0] == "id":
                    self.__dict__[key] = str(value)
                else:
                    self.__dict__[key] = value

    def __str__(self):
        """
        Return the string representation of this class
        """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """
        Updates the public instance attribute:
        updated_at - with the current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        This Method returns a dictionary containing all
        keys/values of __dict__ instance
        """
        objects = self.__dict__.copy()
        objects["created_at"] = self.created_at.isoformat()
        objects["updated_at"] = self.updated_at.isoformat()
        objects["__class__"] = self.__class__.__name__
        return objects
