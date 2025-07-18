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
    def unauthorized() -> Dict[str, Any]:
        """
        Create a standardised 401 error response.

        :return: Standardised error response dictionary
        """
        return {
            "error": "unauthorised",
            "message": "Unauthorised request",
            "status_code": 401,
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
