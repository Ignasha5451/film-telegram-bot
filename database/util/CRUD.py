"""
Module: database/util/CRUD.py
Description: Provides a CRUD (Create, Read, Update, Delete) interface for Peewee models.
"""

from peewee import ModelSelect

from typing import TypeVar, Callable

from database.common.models import db

T = TypeVar("T")


def _create_instance(database: db, model: T, **data) -> None:
    """
    Create a new instance of a Peewee model with the provided data.

    :param database: The Peewee database instance.
    :param model: The Peewee model class.
    :param data: Keyword arguments representing the data for the new instance.
    """
    with database.atomic():
        model.create(**data)


def _read_instance(database: db, model: T, target_user_id: int, count: int) -> ModelSelect:
    """
    Retrieve a specified number of records for a given user ID from a Peewee model.

    :param database: The Peewee database instance.
    :param model: The Peewee model class.
    :param target_user_id: The user ID for which records are to be retrieved.
    :param count: The number of records to retrieve.

    :return: A Peewee query representing the selected records.
    """
    with database.atomic():
        last_n_records = model.select().where(model.user_id == target_user_id).order_by(model.id.desc()).limit(count)
    return last_n_records


class CRUDInterface:
    """
    Provides methods to interact with Peewee models using CRUD operations.
    """
    @staticmethod
    def create() -> Callable:
        """
        Get a function to create a new instance of a Peewee model.

        :return: A function for creating instances of a Peewee model.
        """
        return _create_instance

    @staticmethod
    def read() -> Callable:
        """
        Get a function to read records from a Peewee model.

        :return: A function for reading records from a Peewee model.
        """
        return _read_instance
