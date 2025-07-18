import pytest
from unittest.mock import patch

from connect_client.modules.devices import DevicesAPI
from connect_client.exceptions import (
    ConnectAPIError,
    ResourceNotFoundError,
    UnauthorisedError,
)


class TestDevicesAPI:
    """Test suite for DevicesAPI class"""

    def test_init(self, mock_client):
        """Test DevicesAPI initialization"""
        devices_api = DevicesAPI(mock_client)
        assert devices_api.client == mock_client
        assert devices_api._cache == mock_client.cache

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_device_success(self, mock_request, mock_client, mock_device_response):
        """Test successful device retrieval"""
        mock_request.return_value = mock_device_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_device(1)

        assert result == mock_device_response
        mock_request.assert_called_once()

    def test_get_device_invalid_id_type(self, mock_client):
        """Test get_device with invalid ID type"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="device_id must be a positive integer"):
            devices_api.get_device("invalid")

    def test_get_device_invalid_id_zero(self, mock_client):
        """Test get_device with zero ID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="device_id must be a positive integer"):
            devices_api.get_device(0)

    def test_get_device_invalid_id_negative(self, mock_client):
        """Test get_device with negative ID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="device_id must be a positive integer"):
            devices_api.get_device(-1)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_device_not_found(self, mock_request, mock_client):
        """Test get_device when device not found"""
        mock_request.side_effect = ResourceNotFoundError("Requested resource not found")
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_device(1)

        assert result == {
            "error": "not_found",
            "message": "Device not found",
            "status_code": 404,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_device_unauthorised(self, mock_request, mock_client):
        """Test get_device when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Request not authorised")
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_device(1)

        assert result == {
            "error": "unauthorised",
            "message": "Authorisation failed",
            "status_code": 401,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_device_forbidden(self, mock_request, mock_client):
        """Test get_device when access forbidden"""
        mock_request.side_effect = PermissionError(
            "You are not authorised to access this resource"
        )
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_device(1)

        assert result == {
            "error": "forbidden",
            "message": "You do not have permission to access this resource",
            "status_code": 403,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_device_server_error(self, mock_request, mock_client):
        """Test get_device with server error"""
        mock_request.side_effect = ConnectAPIError(
            "Failed to make request to Connect API"
        )
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_device(1)

        assert result == {
            "error": "api_error",
            "message": "Connect API error",
            "status_code": 500,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_device_api_error(self, mock_request, mock_client):
        """Test get_device with API error"""
        mock_request.side_effect = ConnectAPIError(
            "Failed to make request to Connect API"
        )
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_device(1)

        assert result == {
            "error": "api_error",
            "message": "Connect API error",
            "status_code": 500,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_device_by_uid_success(
        self, mock_request, mock_client, mock_device_response
    ):
        """Test successful device retrieval by UID"""
        mock_request.return_value = mock_device_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_device_by_uid("test-uid-123")

        assert result == mock_device_response
        mock_request.assert_called_once()

    def test_get_device_by_uid_invalid_uid_type(self, mock_client):
        """Test get_device_by_uid with invalid UID type"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="device_uid must be a non-empty string"):
            devices_api.get_device_by_uid(123)

    def test_get_device_by_uid_empty_uid(self, mock_client):
        """Test get_device_by_uid with empty UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="device_uid must be a non-empty string"):
            devices_api.get_device_by_uid("")

    def test_get_device_by_uid_whitespace_uid(self, mock_client):
        """Test get_device_by_uid with whitespace-only UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="device_uid must be a non-empty string"):
            devices_api.get_device_by_uid("   ")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_device_by_uid_not_found(self, mock_request, mock_client):
        """Test get_device_by_uid when device not found"""
        mock_request.side_effect = ResourceNotFoundError("Not found")
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_device_by_uid("test-uid-123")

        assert result == {
            "error": "not_found",
            "message": "Device not found",
            "status_code": 404,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_device_by_uid_unauthorised(self, mock_request, mock_client):
        """Test get_device_by_uid when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Request not authorised")
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_device_by_uid("test-uid-123")

        assert result == {
            "error": "unauthorised",
            "message": "Authorisation failed",
            "status_code": 401,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_device_by_uid_forbidden(self, mock_request, mock_client):
        """Test get_device_by_uid when access forbidden"""
        mock_request.side_effect = PermissionError(
            "You are not authorised to access this resource"
        )
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_device_by_uid("test-uid-123")

        assert result == {
            "error": "forbidden",
            "message": "You do not have permission to access this resource",
            "status_code": 403,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_device_by_uid_server_error(self, mock_request, mock_client):
        """Test get_device_by_uid with server error"""
        mock_request.side_effect = ConnectAPIError("ERR")
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_device_by_uid("test-uid-123")

        assert result == {
            "error": "api_error",
            "message": "Connect API error",
            "status_code": 500,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_device_by_uid_unexpected_exception(self, mock_request, mock_client):
        """Test get_device_by_uid with unexpected exception"""
        mock_request.side_effect = ConnectAPIError(
            "Failed to make request to Connect API"
        )
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_device_by_uid("test-uid-123")

        assert result == {
            "error": "api_error",
            "message": "Connect API error",
            "status_code": 500,
        }

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_url_generation(self, mock_request, mock_client):
        """Test URL generation for endpoints"""
        mock_request.return_value = {"id": 1}
        devices_api = DevicesAPI(mock_client)

        from connect_client.modules.devices.constants import PATH_MAP

        with patch.object(devices_api, "_generate_url") as mock_generate:
            mock_generate.return_value = "https://api.example.com/api/v4/devices/1/"

            devices_api.get_device(1)

            mock_generate.assert_called_once_with("device_by_id", PATH_MAP, device_id=1)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_url_generation_by_uid(self, mock_request, mock_client):
        """Test URL generation for UID endpoint"""
        mock_request.return_value = {"id": 1}
        devices_api = DevicesAPI(mock_client)

        from connect_client.modules.devices.constants import PATH_MAP

        with patch.object(devices_api, "_generate_url") as mock_generate:
            mock_generate.return_value = (
                "https://api.example.com/api/v4/devices/uid/test-uid-123/"
            )

            devices_api.get_device_by_uid("test-uid-123")

            mock_generate.assert_called_once_with(
                "device_by_uid", PATH_MAP, device_uid="test-uid-123"
            )
