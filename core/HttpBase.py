#!/usr/bin/env python3
"""
BaseHttp.py
Written by pollardm
Written: 11/19/24
Description: Base class for HTTP operations.
"""
from abc import ABC, abstractmethod

class BaseHttp(ABC):
    def __init__(self, base_url, verify_ssl=True):
        self.base_url = base_url.rstrip("/")
        self.verify_ssl = verify_ssl

    @abstractmethod
    def request(self, endpoint, method="GET", headers=None, params=None, data=None, json_data=None, auth=None):
        """
        Abstract method for making HTTP requests.

        Args:
            endpoint (str): The API endpoint to hit.
            method (str): HTTP method (GET, POST, etc.).
            headers (dict): Request headers.
            params (dict): Query parameters.
            data (dict): Form data.
            json_data (dict): JSON payload.
            auth (tuple): Authentication credentials.

        Returns:
            Response: The HTTP response object.

        Raises:
            HttpRequestError: If the request fails.
        """
        pass
