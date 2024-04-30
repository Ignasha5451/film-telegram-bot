"""
Module: database/core.py
Description: Demonstrates the usage of CRUDInterface for interacting with Peewee models.
"""

from database.util.CRUD import CRUDInterface
from database.common.models import db, Request

db.connect()
db.create_tables([Request])

crud = CRUDInterface()
