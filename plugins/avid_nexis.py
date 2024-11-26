from urllib.parse import urljoin
import logging
import json
from core.io import HttpRequests

class NexisAdapter(HttpRequests.HttpExecutor):
    # API endpoints configuration remains the same
    api_endpoints = {
        "token": "nxapi/login",
        "external_auth": "externalauth",
        "check_session": "api/checksession",
        "invalidate": "nxapi/logout",
        "users": "api/users",
        "groups": "api/usergroups",
        "workspaces": "api/workspaces",
        "folder_access": "nxapi/fs/node/access",
        "list_folder_acl": "nxapi/fs/node/aclnodes",
        "remove_acl": "nxapi/fs/node/removeacl",
    }

    def __init__(self, username, password, base_url, verify_ssl=False):
        """
        Initialize the Nexis API adapter.
        """
        self.username = username
        self.password = password
        self.token = None
        self.base_url = base_url.rstrip("/")  # Ensure no trailing slash
        super().__init__(base_url, verify_ssl)

    def get_endpoint(self, object_type):
        """
        Retrieve the endpoint for the given object type using urljoin.
        """
        base_endpoint = self.api_endpoints.get(object_type)
        if not base_endpoint:
            raise ValueError(f"Invalid object type '{object_type}'. No endpoint found.")
        return urljoin(self.base_url + "/", base_endpoint)

    def get_token(self):
        """
        Retrieve a Bearer token for authentication.
        """
        endpoint = self.get_endpoint("token")
        payload = json.dumps({"user": self.username, "pass": self.password})

        try:
            response = self.request(endpoint, method="POST", headers=self._get_headers(), data=payload)
            self.token = response.json().get("token")
            if not self.token:
                raise ValueError("Failed to retrieve token.")
            return self.token
        except Exception as e:
            logging.error(f"Failed to retrieve token: {e}")
            raise ValueError("Failed to retrieve token.") from e

    def _get_headers(self):
        """
        Generate standard headers for requests.

        Returns:
            dict: Headers for the request.
        """
        return {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def _ensure_token(self):
        """
        Ensure a valid token exists. Fetch a new one if needed.
        """
        if not self.token:
            self.token = self.get_token()

    def get_object(self, object_type, method="POST"):
        """
        Retrieve or interact with an object using a specified HTTP method.

        Args:
            object_type (str): The object type to fetch.
            method (str): HTTP method to use (e.g., "POST").

        Returns:
            dict: The response JSON containing the object(s).
        """
        endpoint = self.get_endpoint(object_type)
        self._ensure_token()

        # Payload contains the token
        payload = json.dumps({"token": self.token})
        headers = self._get_headers()

        try:
            response = self.request(endpoint, method=method, headers=headers, data=payload)
            return response.json()
        except Exception as e:
            logging.error(f"Failed to retrieve object(s) for '{object_type}' (Method: {method}, Endpoint: {endpoint}): {e}")
            raise ValueError(f"Failed to retrieve object(s) for '{object_type}'.") from e

    def invalidate_token(self):
        """
        Invalidate the current token.

        Returns:
            dict: Response from the server.
        """
        endpoint = self.get_endpoint("invalidate")
        self._ensure_token()

        # Payload contains the token
        payload = json.dumps({"token": self.token})
        headers = self._get_headers()

        try:
            response = self.request(endpoint, method="POST", headers=headers, data=payload)
            self.token = None  # Reset the token
            return response.json()
        except Exception as e:
            logging.error(f"Failed to invalidate token: {e}")
            raise ValueError("Failed to invalidate token.") from e
