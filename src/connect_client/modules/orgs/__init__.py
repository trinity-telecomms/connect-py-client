from connect_client.exceptions import ConnectAPIError
from connect_client.mixins import ResourceMixin
from .constants import PATH_MAP


class OrgsAPI(ResourceMixin):
    def get_company(self, company_id):
        """
        GET a company by ID.
        :param company_id:
        :return: Company object
        """
        url = self._generate_url("company_by_id", PATH_MAP, company_id=company_id)

        try:
            status, response = self.make_get_request(url)
            return response
        except Exception as e:
            print(e)
            raise ConnectAPIError("Failed to get company from Connect API")
