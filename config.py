"""
Module: config.py
Description: Defines settings and loads environment variables from a .env file.
"""

import os

from pydantic import BaseModel, SecretStr
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    """
    Settings model to store sensitive API tokens securely.
    """
    telebot_token: SecretStr
    rapid_key: SecretStr
    rapid_host: SecretStr


# Initialize settings with values from environment variables
settings = Settings(
    telebot_token=os.getenv("TELEBOT_TOKEN"),
    rapid_key=os.getenv("RAPID_KEY"),
    rapid_host=os.getenv("RAPID_HOST")
)
