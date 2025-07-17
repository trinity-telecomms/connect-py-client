from connect_client.exceptions import ConnectAPIError
from connect_client.mixins import ResourceMixin
from .constants import PATH_MAP


class AuthAPI(ResourceMixin):
    def _get_credentials(self):
        """
        Retrieve the email and password from the client instance
        credentials configuration. Returns a dictionary with "email" and "password"
        :return:
        """
        return self.client.credentials

    def login(self):
        """
        Get the credentials from the client instance configuration and attempt to
        log in. Return the JSON response that includes the authentication token.

        :return:
        """
        url = self._generate_url("login", PATH_MAP)
        data = self._get_credentials()
        headers = self._get_default_headers()

        try:
            status, response = self.make_post_request(url, headers=headers, json=data)
            return response
        except Exception:
            raise ConnectAPIError("Could not login to Connect API")
