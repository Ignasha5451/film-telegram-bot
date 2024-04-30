"""
Module: film_API/core.py
Description: Provides utilities for making API requests with rate limiting.
"""

import time
from typing import Callable

import requests

from config import settings


def inhibitor(func: Callable) -> Callable:
    """
    Decorator function to add a rate-limiting delay of 1 second to API requests.

    :param func:The function to be decorated.

    :return: The decorated function.
    """
    def wrapper(*args, **kwargs) -> any:
        """
        Wrapper function to add a rate-limiting delay before calling the decorated function.

        :param args: Positional arguments passed to the decorated function.
        :param kwargs: Keyword arguments passed to the decorated function.

        :return: The result of the decorated function.
        """
        result = func(*args, **kwargs)
        time.sleep(1)
        return result

    return wrapper


# Define the base URL for API requests
URL = "https://ott-details.p.rapidapi.com"


@inhibitor
def api_request(request: str, params: dict) -> dict:
    """
    Make an API request to the specified endpoint with the provided parameters.

    :param request: The endpoint of the API.
    :param params: The parameters to be sent with the request.

    :return: The JSON response from the API.
    """
    url = f"{URL}/{request}"

    headers = {
        "X-RapidAPI-Key": settings.rapid_key.get_secret_value(),
        "X-RapidAPI-Host": settings.rapid_host.get_secret_value()
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get("results", response.json())
    except requests.RequestException as e:
        print(f"Error making API request: {e}")
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
