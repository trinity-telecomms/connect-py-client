import requests

from trinity_connect_client.exceptions import (
    ConnectAPIError,
    ResourceNotFoundError,
    UnauthorisedError,
)


class ResourceMixin:
    def __init__(self, client):
        self.client = client

    def _url(self, path: str) -> str:
        """
        Build a full API URL from a path string.

        :param path: The URL path (e.g., "devices/123" or "devices/uid/abc-123")
        :return: Full URL including base API URL
        """
        # Remove leading slash if present for consistency
        path = path.lstrip("/")
        return f"{self.client.api_url}/{path}"

    @staticmethod
    def _get_default_headers():
        """
        Constructs the defaults headers required for Connect API requests. The
        default headers do not include the Authorization header which is required
        for most endpoints. Use _get_auth_headers() instead.
        """
        return {"Content-Type": "application/json", "Accept": "application/json"}

    def _get_auth_headers(self):
        default_headers = self._get_default_headers()
        return {
            **default_headers,
            "Authorization": f"Bearer {self.client.token}",
        }

    def make_post_request(self, url, headers=None, json=None):
        request_headers = self._get_auth_headers() if not headers else headers

        try:
            response = requests.post(url, headers=request_headers, json=json)
        except Exception:
            raise ConnectAPIError("Failed to make request to Connect API")

        if response.status_code == 401:
            raise UnauthorisedError("Authorisation failed")
        if response.status_code == 403:
            raise PermissionError("You are not authorised to access this resource")
        if response.status_code == 404:
            raise ResourceNotFoundError("Requested resource not found")
        if response.status_code == 400:
            try:
                error_data = response.json()
                error_msg = (
                    error_data.get("detail")
                    or error_data.get("error")
                    or str(error_data)
                )
            except Exception:
                error_msg = response.text or "Bad request"
            raise ValueError(f"Validation error: {error_msg}")
        if response.status_code not in [200, 201]:
            print(response.text)
            raise ConnectAPIError(
                f"Connect API returned unexpected status code: {response.status_code}"
            )

        return response.json()

    def make_patch_request(self, url, headers=None, json=None):
        request_headers = self._get_auth_headers() if not headers else headers

        try:
            response = requests.patch(url, headers=request_headers, json=json)
        except Exception:
            raise ConnectAPIError("Failed to make request to Connect API")

        if response.status_code == 401:
            raise UnauthorisedError("Authorisation failed")
        if response.status_code == 403:
            raise PermissionError("You are not authorised to access this resource")
        if response.status_code == 404:
            raise ResourceNotFoundError("Requested resource not found")
        if response.status_code == 400:
            try:
                error_data = response.json()
                error_msg = (
                    error_data.get("detail")
                    or error_data.get("error")
                    or str(error_data)
                )
            except Exception:
                error_msg = response.text or "Bad request"
            raise ValueError(f"Validation error: {error_msg}")
        if response.status_code != 200:
            raise ConnectAPIError(
                f"Connect API returned unexpected status code: {response.status_code}"
            )

        return response.json()

    def make_get_request(self, url, headers=None, params=None):
        request_headers = self._get_auth_headers() if not headers else headers

        try:
            response = requests.get(url, headers=request_headers, params=params)
        except Exception:
            raise ConnectAPIError("Failed to make request to Connect API")

        if response.status_code == 401:
            raise UnauthorisedError("Authorisation failed")
        if response.status_code == 403:
            raise PermissionError("You are not authorised to access this resource")
        if response.status_code == 404:
            raise ResourceNotFoundError("Requested resource not found")
        if response.status_code != 200:
            raise ConnectAPIError("Connect API returned unexpected status code")

        return response.json()

    def make_delete_request(self, url, headers=None):
        request_headers = self._get_auth_headers() if not headers else headers

        try:
            response = requests.delete(url, headers=request_headers)
        except Exception:
            raise ConnectAPIError("Failed to make request to Connect API")

        if response.status_code == 401:
            raise UnauthorisedError("Authorisation failed")
        if response.status_code == 403:
            raise PermissionError("You are not authorised to access this resource")
        if response.status_code == 404:
            raise ResourceNotFoundError("Requested resource not found")
        if response.status_code not in [200, 204]:
            raise ConnectAPIError(
                f"Connect API returned unexpected status code: {response.status_code}"
            )

        return None

    def make_put_request(self, url, headers=None, json=None):
        request_headers = self._get_auth_headers() if not headers else headers

        try:
            response = requests.put(url, headers=request_headers, json=json)
        except Exception:
            raise ConnectAPIError("Failed to make request to Connect API")

        if response.status_code == 401:
            raise UnauthorisedError("Authorisation failed")
        if response.status_code == 403:
            raise PermissionError("You are not authorised to access this resource")
        if response.status_code == 404:
            raise ResourceNotFoundError("Requested resource not found")
        if response.status_code == 400:
            try:
                error_data = response.json()
                error_msg = (
                    error_data.get("detail")
                    or error_data.get("error")
                    or str(error_data)
                )
            except Exception:
                error_msg = response.text or "Bad request"
            raise ValueError(f"Validation error: {error_msg}")
        if response.status_code != 200:
            raise ConnectAPIError(
                f"Connect API returned unexpected status code: {response.status_code}"
            )

        return response.json()

    def get_linked_resource(self, url):
        """
        Helper method to get a linked resource from a previous interaction.
        Some APIs return URLs in the response for related resources, previous or next
        pages etc.

        :param url:
        :return:
        """
        return self.make_get_request(url)
