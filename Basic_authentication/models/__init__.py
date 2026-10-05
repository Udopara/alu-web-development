#!/usr/bin/env python3
""" Models package initialization
"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
DATA = storage.all()
storage.reload()
