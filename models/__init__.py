#!/bin/usr/python3
"""
Init for models module
code is executed whenever the package is imported
"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
