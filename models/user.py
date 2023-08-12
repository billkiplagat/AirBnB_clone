#!/usr/bin/python3
"""Importing base_model module"""
from models.base_model import BaseModel


class User(BaseModel):
    """User class representation"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
