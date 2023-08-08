#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime


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
            "Using *args"
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
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
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """
        Method returns a dictionary containing all
        keys/values of __dict__ instance
        """
        objects = {}
        for key, values in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                """
                isoformat() used to represent a datetime object 
                in a string format following the ISO 8601 standard
                """
                objects[key] = values.isoformat()
            else:
                objects[key] = values
        objects["__class__"] = self.__class__.__name__
        return objects
