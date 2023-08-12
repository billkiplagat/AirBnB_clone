#!/usr/bin/python3
"""Importing base_model module"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Review class representation"""
    place_id = ""
    user_id = ""
    text = ""
