from connect_client.exceptions import ConnectAPIError
from connect_client.mixins import ResourceMixin
from .constants import PATH_MAP


class OrgsAPI(ResourceMixin):
    def get_company(self, company_id: int):
        """
        GET a company by ID.

        :param company_id:
        :return: A Company object
        """
        url = self._generate_url("company_by_id", PATH_MAP, company_id=company_id)

        try:
            status, response = self.make_get_request(url)
            return response
        except Exception as e:
            print(e)
            raise ConnectAPIError("Failed to get company from Connect API")

    def get_company_folders(self, company_id: int, **filters):
        """
        GET company folders for a given company ID.

        :param company_id:
        :return: List of folder objects
        """
        url = self._generate_url("company_folders", PATH_MAP, company_id=company_id)

        try:
            status, response = self.make_get_request(url, params=filters)
            return response
        except Exception as e:
            print(e)
            raise ConnectAPIError("Failed to get company from Connect API")
