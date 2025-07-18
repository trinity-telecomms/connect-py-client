from typing import Dict, Any


class ErrorResponse:
    """Factory class for creating consistent error response dictionaries."""

    @staticmethod
    def not_found(resource_type: str) -> Dict[str, Any]:
        """
        Create a standardised 404 error response.

        :param resource_type: Type of resource (e.g., "Company", "Device")
        :return: Standardised error response dictionary
        """
        return {
            "error": "not_found",
            "message": f"{resource_type} not found",
            "status_code": 404,
        }

    @staticmethod
    def unauthorised() -> Dict[str, Any]:
        """
        Create a standardised 401 error response.

        :return: Standardised error response dictionary
        """
        return {
            "error": "unauthorised",
            "message": "Authorisation failed",
            "status_code": 401,
        }

    @staticmethod
    def forbidden() -> Dict[str, Any]:
        """
        Create a standardised 403 error response.

        :return: Standardised error response dictionary
        """
        return {
            "error": "forbidden",
            "message": "You do not have permission to access this resource",
            "status_code": 403,
        }

    @staticmethod
    def api_error() -> Dict[str, Any]:
        """
        Create a standardised 500 error response.

        :return: Standardised error response dictionary
        """
        return {
            "error": "api_error",
            "message": "Connect API error",
            "status_code": 500,
        }
