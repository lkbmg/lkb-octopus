import logging
import json
from urllib.parse import urljoin
from core.io import HttpRequests


class AirtableAdapter(HttpRequests.HttpExecutor):
    """
    Adapter for interacting with the Airtable API.
    Handles authentication and common operations with dynamic endpoint support.
    """

    api_endpoints = {
        "base": "v0/meta/bases",
        "workspace_collaborators": "v0/meta/workspaces",
        "oauth": "oauth2/v1/authorize",
        "list_records": "v0/{base_id}/{table_id_or_name}/listRecords",
    }

    def __init__(self, base_url, token, verify_ssl=False):
        """
        Initialize the Airtable API adapter.

        Args:
            base_url (str): Base URL for Airtable API.
            token (str): Airtable API token.
            verify_ssl (bool): Whether to verify SSL certificates. Default is False.
        """
        self.token = token
        self.base_url = base_url.rstrip("/")  # Ensure no trailing slash
        super().__init__(base_url, verify_ssl)

    def get_endpoint(self, endpoint_name, **kwargs):
        """
        Construct the endpoint URL dynamically based on the API name and parameters.

        Args:
            endpoint_name (str): Name of the API endpoint.
            **kwargs: Additional parameters for URL formatting.

        Returns:
            str: The constructed endpoint URL.

        Raises:
            ValueError: If the endpoint name is invalid or missing required parameters.
        """
        base_endpoint = self.api_endpoints.get(endpoint_name)
        if not base_endpoint:
            raise ValueError(f"Invalid endpoint name '{endpoint_name}'. No endpoint found.")
        return urljoin(self.base_url + "/", base_endpoint.format(**kwargs))

    def _get_headers(self):
        """
        Generate standard headers for requests, including authorization.

        Returns:
            dict: Headers for the request.
        """
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def list_records(self, base_id, table_id_or_name, params=None, payload=None):
        """
        Fetch all records from a table using the POST-based listRecords endpoint.

        Args:
            base_id (str): The Airtable base ID.
            table_id_or_name (str): The Airtable table ID or name.
            params (dict, optional): Query parameters for timezone, locale, etc.
            payload (dict, optional): Body parameters like fields, filters, sorting, etc.

        Returns:
            list: All records from the table.
        """
        all_records = []
        offset = None
        params = params or {}
        payload = payload or {}

        try:
            while True:
                if offset:
                    payload["offset"] = offset

                endpoint = self.get_endpoint("list_records", base_id=base_id, table_id_or_name=table_id_or_name)
                response = self.request(
                    endpoint,
                    method="POST",
                    headers=self._get_headers(),
                    params=params,
                    data=json.dumps(payload),
                ).json()

                all_records.extend(response.get("records", []))
                offset = response.get("offset")

                if not offset:
                    break

        except Exception as e:
            logging.error(f"Exception occurred while fetching records: {e}")
            raise ValueError("Failed to fetch records.") from e

        return all_records

    def fetch_record(self, base_id, table_id_or_name, record_id):
        """
        Fetch a specific record from an Airtable table.

        Args:
            base_id (str): The Airtable base ID.
            table_id_or_name (str): The Airtable table ID or name.
            record_id (str): The ID of the record to fetch.

        Returns:
            dict: The record data.
        """
        try:
            endpoint = f"{self.base_url}/v0/{base_id}/{table_id_or_name}/{record_id}"
            response = self.request(endpoint, method="GET", headers=self._get_headers())
            return response.json()
        except Exception as e:
            logging.error(f"Failed to fetch record {record_id}: {e}")
            raise ValueError("Failed to fetch record.") from e

    def create_record(self, base_id, table_id_or_name, fields):
        """
        Create a new record in an Airtable table.

        Args:
            base_id (str): The Airtable base ID.
            table_id_or_name (str): The Airtable table ID or name.
            fields (dict): Fields for the new record.

        Returns:
            dict: The created record data.
        """
        try:
            endpoint = f"{self.base_url}/v0/{base_id}/{table_id_or_name}"
            response = self.request(
                endpoint,
                method="POST",
                headers=self._get_headers(),
                data=json.dumps({"fields": fields}),
            )
            return response.json()
        except Exception as e:
            logging.error(f"Failed to create record: {e}")
            raise ValueError("Failed to create record.") from e

    def update_record(self, base_id, table_id_or_name, record_id, fields):
        """
        Update a specific record in an Airtable table.

        Args:
            base_id (str): The Airtable base ID.
            table_id_or_name (str): The Airtable table ID or name.
            record_id (str): The ID of the record to update.
            fields (dict): Fields to update.

        Returns:
            dict: The updated record data.
        """
        try:
            endpoint = f"{self.base_url}/v0/{base_id}/{table_id_or_name}/{record_id}"
            response = self.request(
                endpoint,
                method="PATCH",
                headers=self._get_headers(),
                data=json.dumps({"fields": fields}),
            )
            return response.json()
        except Exception as e:
            logging.error(f"Failed to update record {record_id}: {e}")
            raise ValueError("Failed to update record.") from e

    def delete_record(self, base_id, table_id_or_name, record_id):
        """
        Delete a specific record in an Airtable table.

        Args:
            base_id (str): The Airtable base ID.
            table_id_or_name (str): The Airtable table ID or name.
            record_id (str): The ID of the record to delete.

        Returns:
            dict: The response from the delete operation.
        """
        try:
            endpoint = f"{self.base_url}/v0/{base_id}/{table_id_or_name}/{record_id}"
            response = self.request(endpoint, method="DELETE", headers=self._get_headers())
            return response.json()
        except Exception as e:
            logging.error(f"Failed to delete record {record_id}: {e}")
            raise ValueError("Failed to delete record.") from e
