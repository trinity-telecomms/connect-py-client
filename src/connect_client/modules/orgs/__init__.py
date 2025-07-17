import logging
from typing import Dict, List, Any

from connect_client.exceptions import ConnectAPIError
from connect_client.mixins import ResourceMixin
from .constants import PATH_MAP

logger = logging.getLogger(__name__)


class OrgsAPI(ResourceMixin):
    def get_company(self, company_id: int) -> Dict[str, Any]:
        """
        GET a company by ID.

        :param company_id: The ID of the company to retrieve
        :return: A Company object as dictionary
        :raises ConnectAPIError: If the API request fails
        :raises ValueError: If company_id is not a positive integer
        """
        if not isinstance(company_id, int) or company_id <= 0:
            raise ValueError("company_id must be a positive integer")

        url = self._generate_url("company_by_id", PATH_MAP, company_id=company_id)

        try:
            status, response = self.make_get_request(url)

            if status == 404:
                raise ConnectAPIError(f"Company with ID {company_id} not found")
            elif status == 403:
                raise ConnectAPIError("Insufficient permissions to access company")
            elif status != 200:
                raise ConnectAPIError(f"API returned status {status}")

            return response
        except ConnectAPIError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error getting company {company_id}: {e}")
            raise ConnectAPIError(f"Failed to get company from Connect API: {str(e)}")

    def get_company_folders(self, company_id: int, **filters) -> List[Dict[str, Any]]:
        """
        GET company folders for a given company ID.

        :param company_id: The ID of the company whose folders to retrieve
        :param filters: Optional filters to apply to the request
        :return: List of folder objects as dictionaries
        :raises ConnectAPIError: If the API request fails
        :raises ValueError: If company_id is not a positive integer
        """
        if not isinstance(company_id, int) or company_id <= 0:
            raise ValueError("company_id must be a positive integer")

        url = self._generate_url("company_folders", PATH_MAP, company_id=company_id)

        try:
            status, response = self.make_get_request(url, params=filters)

            if status == 404:
                raise ConnectAPIError(f"Company with ID {company_id} not found")
            elif status == 403:
                raise ConnectAPIError(
                    "Insufficient permissions to access company folders"
                )
            elif status != 200:
                raise ConnectAPIError(f"API returned status {status}")

            return response if isinstance(response, list) else []
        except ConnectAPIError:
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error getting company folders for {company_id}: {e}"
            )
            raise ConnectAPIError(
                f"Failed to get company folders from Connect API: {str(e)}"
            )
