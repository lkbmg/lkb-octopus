"""
HttpExecutor.py
Written by pollardm
Written: 11/19/24
Description: HTTP executor for making REST API requests.
"""
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .HttpBase import BaseHttp, HttpRequestError


class HttpExecutor(BaseHttp):
    def __init__(self, base_url, verify_ssl=True):
        super().__init__(base_url, verify_ssl)
        self.session = self._initialize_session()

    def _initialize_session(self):
        """Initialize a requests session with retry logic."""
        session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def request(self, endpoint, method="GET", headers=None, params=None, data=None, json_data=None, auth=None):
        """
        Make an HTTP request.

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
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json_data,
                auth=auth,
                verify=self.verify_ssl,
                timeout=10,
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP request failed: {e}")
            raise HttpRequestError(url, getattr(e.response, "status_code", None), str(e)) from e

    def close(self):
        """Close the requests session."""
        self.session.close()
