"""
Module: database/common/models.py
Description: Defines models for storing user-bot interaction history.
"""

from datetime import datetime

import peewee as pw

db = pw.SqliteDatabase("database/db/history.db")


class BaseModel(pw.Model):
    """
    Base model for all other models, sets up the database connection.
    """
    class Meta:
        database = db


class Request(BaseModel):
    """
    Model representing user-bot interaction requests.
    """
    user_id = pw.IntegerField()
    user_request = pw.TextField()
    bot_response = pw.TextField()
    created_at = pw.DateTimeField(default=datetime.now)

    class Meta:
        """
        Metadata for the Request model.
        """
        table_name = "requests"
