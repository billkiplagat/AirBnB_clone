#!/usr/bin/python3
"""Importing base_model module"""
from models.base_model import BaseModel


class City(BaseModel):
    """City class representation"""
    state_id = ""
    name = ""
