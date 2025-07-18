import pytest
from unittest.mock import patch

from connect_client.modules.orgs import OrgsAPI
from connect_client.exceptions import (
    ConnectAPIError,
    ResourceNotFoundError,
    UnauthorizedError,
)


class TestOrgsAPI:
    """Test suite for OrgsAPI class with updated pattern"""

    def test_init(self, mock_client):
        """Test OrgsAPI initialization"""
        orgs_api = OrgsAPI(mock_client)
        assert orgs_api.client == mock_client
        assert orgs_api._cache == mock_client.cache

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_company_success(
        self, mock_request, mock_client, mock_company_response
    ):
        """Test successful company retrieval"""
        mock_request.return_value = mock_company_response
        orgs_api = OrgsAPI(mock_client)

        result = orgs_api.get_company(1)

        assert result == mock_company_response
        mock_request.assert_called_once()

    def test_get_company_invalid_id_type(self, mock_client):
        """Test get_company with invalid ID type"""
        orgs_api = OrgsAPI(mock_client)

        with pytest.raises(ValueError, match="company_id must be a positive integer"):
            orgs_api.get_company("invalid")

    def test_get_company_invalid_id_zero(self, mock_client):
        """Test get_company with zero ID"""
        orgs_api = OrgsAPI(mock_client)

        with pytest.raises(ValueError, match="company_id must be a positive integer"):
            orgs_api.get_company(0)

    def test_get_company_invalid_id_negative(self, mock_client):
        """Test get_company with negative ID"""
        orgs_api = OrgsAPI(mock_client)

        with pytest.raises(ValueError, match="company_id must be a positive integer"):
            orgs_api.get_company(-1)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_company_not_found(self, mock_request, mock_client):
        """Test get_company when company not found"""
        mock_request.side_effect = ResourceNotFoundError("Requested resource not found")
        orgs_api = OrgsAPI(mock_client)

        result = orgs_api.get_company(1)

        assert result == {
            "error": "not_found",
            "message": "Company not found",
            "status_code": 404,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_company_unauthorized(self, mock_request, mock_client):
        """Test get_company when access unauthorized"""
        mock_request.side_effect = UnauthorizedError("Request not authorised")
        orgs_api = OrgsAPI(mock_client)

        result = orgs_api.get_company(1)

        assert result == {
            "error": "unauthorised",
            "message": "Unauthorised request",
            "status_code": 401,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_company_server_error(self, mock_request, mock_client):
        """Test get_company with server error"""
        mock_request.side_effect = ConnectAPIError(
            "Failed to make request to Connect API"
        )
        orgs_api = OrgsAPI(mock_client)

        result = orgs_api.get_company(1)

        assert result == {
            "error": "api_error",
            "message": "Connect API error",
            "status_code": 500,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_company_api_error(self, mock_request, mock_client):
        """Test get_company with API error"""
        mock_request.side_effect = ConnectAPIError(
            "Failed to make request to Connect API"
        )
        orgs_api = OrgsAPI(mock_client)

        result = orgs_api.get_company(1)

        assert result == {
            "error": "api_error",
            "message": "Connect API error",
            "status_code": 500,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_company_folders_success(
        self, mock_request, mock_client, mock_company_folders_response
    ):
        """Test successful company folders retrieval"""
        mock_request.return_value = mock_company_folders_response
        orgs_api = OrgsAPI(mock_client)

        result = orgs_api.get_company_folders(1)

        assert result == mock_company_folders_response
        mock_request.assert_called_once()

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_company_folders_with_filters(
        self, mock_request, mock_client, mock_company_folders_response
    ):
        """Test company folders retrieval with filters"""
        mock_request.return_value = mock_company_folders_response
        orgs_api = OrgsAPI(mock_client)

        filters = {"active": True, "limit": 10}
        result = orgs_api.get_company_folders(1, **filters)

        assert result == mock_company_folders_response
        mock_request.assert_called_once()
        # Check that params were passed correctly
        call_args = mock_request.call_args
        assert call_args[1]["params"] == filters

    def test_get_company_folders_invalid_id_type(self, mock_client):
        """Test get_company_folders with invalid ID type"""
        orgs_api = OrgsAPI(mock_client)

        with pytest.raises(ValueError, match="company_id must be a positive integer"):
            orgs_api.get_company_folders("invalid")

    def test_get_company_folders_invalid_id_zero(self, mock_client):
        """Test get_company_folders with zero ID"""
        orgs_api = OrgsAPI(mock_client)

        with pytest.raises(ValueError, match="company_id must be a positive integer"):
            orgs_api.get_company_folders(0)

    def test_get_company_folders_invalid_id_negative(self, mock_client):
        """Test get_company_folders with negative ID"""
        orgs_api = OrgsAPI(mock_client)

        with pytest.raises(ValueError, match="company_id must be a positive integer"):
            orgs_api.get_company_folders(-1)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_company_folders_not_found(self, mock_request, mock_client):
        """Test get_company_folders when company not found"""
        mock_request.side_effect = ResourceNotFoundError("Not found")
        orgs_api = OrgsAPI(mock_client)

        result = orgs_api.get_company_folders(1)

        assert result == {
            "error": "not_found",
            "message": "Company not found",
            "status_code": 404,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_company_folders_unauthorized(self, mock_request, mock_client):
        """Test get_company_folders when access unauthorized"""
        mock_request.side_effect = UnauthorizedError("Request not authorised")
        orgs_api = OrgsAPI(mock_client)

        result = orgs_api.get_company_folders(1)

        assert result == {
            "error": "unauthorised",
            "message": "Unauthorised request",
            "status_code": 401,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_company_folders_server_error(self, mock_request, mock_client):
        """Test get_company_folders with server error"""
        mock_request.side_effect = ConnectAPIError("ERR")
        orgs_api = OrgsAPI(mock_client)

        result = orgs_api.get_company_folders(1)

        assert result == {
            "error": "api_error",
            "message": "Connect API error",
            "status_code": 500,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_company_folders_unexpected_exception(self, mock_request, mock_client):
        """Test get_company_folders with unexpected exception"""
        mock_request.side_effect = ConnectAPIError(
            "Failed to make request to Connect API"
        )
        orgs_api = OrgsAPI(mock_client)

        result = orgs_api.get_company_folders(1)

        assert result == {
            "error": "api_error",
            "message": "Connect API error",
            "status_code": 500,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_url_generation(self, mock_request, mock_client):
        """Test URL generation for endpoints"""
        mock_request.return_value = {"id": 1}
        orgs_api = OrgsAPI(mock_client)

        from connect_client.modules.orgs.constants import PATH_MAP

        with patch.object(orgs_api, "_generate_url") as mock_generate:
            mock_generate.return_value = (
                "https://api.example.com/api/v4/orgs/company/1/"
            )

            orgs_api.get_company(1)

            mock_generate.assert_called_once_with(
                "company_by_id", PATH_MAP, company_id=1
            )
