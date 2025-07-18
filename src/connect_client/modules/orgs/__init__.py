from typing import Dict, List, Any, Union

from connect_client.exceptions import UnauthorizedError, ResourceNotFoundError
from connect_client.exceptions.error_responses import ErrorResponse
from connect_client.mixins import ResourceMixin
from .constants import PATH_MAP


class OrgsAPI(ResourceMixin):
    def get_company(self, company_id: int) -> Dict[str, Any]:
        """
        GET a company by ID.

        :param company_id: The ID of the company to retrieve
        :return: A Company object as dictionary or error response
        :raises ValueError: If company_id is not a positive integer
        """
        if not isinstance(company_id, int) or company_id <= 0:
            raise ValueError("company_id must be a positive integer")

        url = self._generate_url("company_by_id", PATH_MAP, company_id=company_id)

        try:
            return self.make_get_request(url)
        except UnauthorizedError:
            return ErrorResponse.unauthorized()
        except ResourceNotFoundError:
            return ErrorResponse.not_found("Company")
        except Exception:
            return ErrorResponse.api_error()

    def get_company_folders(self, company_id: int, **filters) -> Union[
        List[Dict[str, Any]], Dict[str, Any]]:
        """
        GET company folders for a given company ID.

        :param company_id: The ID of the company whose folders to retrieve
        :param filters: Optional filters to apply to the request
        :return: List of folder objects as dictionaries or error response
        :raises ValueError: If company_id is not a positive integer
        """
        if not isinstance(company_id, int) or company_id <= 0:
            raise ValueError("company_id must be a positive integer")

        url = self._generate_url("company_folders", PATH_MAP, company_id=company_id)

        try:
            return self.make_get_request(url, params=filters)
        except UnauthorizedError:
            return ErrorResponse.unauthorized()
        except ResourceNotFoundError:
            return ErrorResponse.not_found("Company")
        except Exception:
            return ErrorResponse.api_error()
