import sys, os, logging, requests, datetime, pytz
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from core.HttpBase import BaseHttp
from core.Exceptions import HttpRequestError
from core.utility.Normalize import Normalization


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)+'/../'))

class HttpExecutor(BaseHttp):
    def __init__(self, base_url, verify_ssl=True):
        super().__init__(base_url, verify_ssl)
        self.session = self._initialize_session()
        self.base_url = Normalization.normalize_url(base_url)

    def _initialize_session(self):
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
        # Normalize and validate inputs
        endpoint = Normalization.normalize_whitespace(endpoint)
        headers = Normalization.normalize_dict(headers) if headers else {}
        params = Normalization.normalize_dict(params) if params else {}
        json_data = Normalization.normalize_json(json_data) if json_data else None

        # Check if `endpoint` is a full URL or a relative path
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            url = endpoint  # Use the full URL directly
        else:
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
        self.session.close()
