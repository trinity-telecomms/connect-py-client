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
        """Test DevicesAPI initialisation"""
        devices_api = DevicesAPI(mock_client)
        assert devices_api.client == mock_client

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_success(self, mock_request, mock_client, mock_device_response):
        """Test successful device retrieval"""
        mock_request.return_value = mock_device_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get(1)

        assert result == mock_device_response
        mock_request.assert_called_once()

    def test_get_invalid_id_type(self, mock_client):
        """Test get with invalid ID type"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.get("invalid")

    def test_get_invalid_id_zero(self, mock_client):
        """Test get with zero ID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.get(0)

    def test_get_invalid_id_negative(self, mock_client):
        """Test get with negative ID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.get(-1)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_not_found(self, mock_request, mock_client):
        """Test get when device not found"""
        mock_request.side_effect = ResourceNotFoundError("Requested resource not found")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ResourceNotFoundError, match="Requested resource not found"):
            devices_api.get(1)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_unauthorised(self, mock_request, mock_client):
        """Test get when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Request not authorised")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(UnauthorisedError, match="Request not authorised"):
            devices_api.get(1)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_forbidden(self, mock_request, mock_client):
        """Test get when access forbidden"""
        mock_request.side_effect = PermissionError(
            "You are not authorised to access this resource"
        )
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(
            PermissionError, match="You are not authorised to access this resource"
        ):
            devices_api.get(1)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_server_error(self, mock_request, mock_client):
        """Test get with server error"""
        mock_request.side_effect = ConnectAPIError(
            "Failed to make request to Connect API"
        )
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(
            ConnectAPIError, match="Failed to make request to Connect API"
        ):
            devices_api.get(1)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_by_uid_success(self, mock_request, mock_client, mock_device_response):
        """Test successful device retrieval by UID"""
        mock_request.return_value = mock_device_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_by_uid("test-uid-123")

        assert result == mock_device_response
        mock_request.assert_called_once()

    def test_get_by_uid_invalid_uid_type(self, mock_client):
        """Test get_by_uid with invalid UID type"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.get_by_uid(123)

    def test_get_by_uid_empty_uid(self, mock_client):
        """Test get_by_uid with empty UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.get_by_uid("")

    def test_get_by_uid_whitespace_uid(self, mock_client):
        """Test get_by_uid with whitespace-only UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.get_by_uid("   ")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_by_uid_not_found(self, mock_request, mock_client):
        """Test get_by_uid when device not found"""
        mock_request.side_effect = ResourceNotFoundError("Not found")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ResourceNotFoundError, match="Not found"):
            devices_api.get_by_uid("test-uid-123")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_by_uid_unauthorised(self, mock_request, mock_client):
        """Test get_by_uid when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Request not authorised")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(UnauthorisedError, match="Request not authorised"):
            devices_api.get_by_uid("test-uid-123")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_by_uid_forbidden(self, mock_request, mock_client):
        """Test get_by_uid when access forbidden"""
        mock_request.side_effect = PermissionError(
            "You are not authorised to access this resource"
        )
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(
            PermissionError, match="You are not authorised to access this resource"
        ):
            devices_api.get_by_uid("test-uid-123")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_by_uid_server_error(self, mock_request, mock_client):
        """Test get_by_uid with server error"""
        mock_request.side_effect = ConnectAPIError("ERR")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ConnectAPIError, match="ERR"):
            devices_api.get_by_uid("test-uid-123")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_by_uid_unexpected_exception(self, mock_request, mock_client):
        """Test get_by_uid with unexpected exception"""
        mock_request.side_effect = ConnectAPIError(
            "Failed to make request to Connect API"
        )
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(
            ConnectAPIError, match="Failed to make request to Connect API"
        ):
            devices_api.get_by_uid("test-uid-123")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_url_generation(self, mock_request, mock_client):
        """Test URL generation for endpoints"""
        mock_request.return_value = {"id": 1}
        devices_api = DevicesAPI(mock_client)

        with patch.object(devices_api, "_url") as mock_url:
            mock_url.return_value = "https://api.example.com/api/v4/devices/1/"

            devices_api.get(1)

            mock_url.assert_called_once_with("devices/1/")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_url_generation_by_uid(self, mock_request, mock_client):
        """Test URL generation for UID endpoint"""
        mock_request.return_value = {"id": 1}
        devices_api = DevicesAPI(mock_client)

        with patch.object(devices_api, "_url") as mock_url:
            mock_url.return_value = (
                "https://api.example.com/api/v4/devices/uid/test-uid-123/"
            )

            devices_api.get_by_uid("test-uid-123")

            mock_url.assert_called_once_with("devices/uid/test-uid-123/")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_latest_data_by_uid_success(
        self, mock_request, mock_client, mock_device_response
    ):
        """Test successful latest data retrieval by UID"""
        mock_request.return_value = mock_device_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_latest_data_by_uid("test-uid-123")

        assert result == mock_device_response
        mock_request.assert_called_once()

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_latest_data_by_uid_with_filters(
        self, mock_request, mock_client, mock_device_response
    ):
        """Test latest data retrieval with filters"""
        mock_request.return_value = mock_device_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_latest_data_by_uid(
            "test-uid-123", limit="10", offset="0"
        )

        assert result == mock_device_response
        mock_request.assert_called_once_with(
            mock_request.call_args[0][0], params={"limit": "10", "offset": "0"}
        )

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_events_by_uid_success(
        self, mock_request, mock_client, mock_device_response
    ):
        """Test successful events retrieval by UID"""
        mock_request.return_value = mock_device_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_events_by_uid("test-uid-123")

        assert result == mock_device_response
        mock_request.assert_called_once()

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_events_by_uid_with_filters(
        self, mock_request, mock_client, mock_device_response
    ):
        """Test events retrieval with filters"""
        mock_request.return_value = mock_device_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_events_by_uid("test-uid-123", type="alert", limit="5")

        assert result == mock_device_response
        mock_request.assert_called_once_with(
            mock_request.call_args[0][0], params={"type": "alert", "limit": "5"}
        )

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_url_generation_latest_data(self, mock_request, mock_client):
        """Test URL generation for latest data endpoint"""
        mock_request.return_value = {"data": "latest"}
        devices_api = DevicesAPI(mock_client)

        with patch.object(devices_api, "_url") as mock_url:
            mock_url.return_value = (
                "https://api.example.com/api/v4/devices/uid/test-uid-123/data/latest/"
            )

            devices_api.get_latest_data_by_uid("test-uid-123")

            mock_url.assert_called_once_with("devices/uid/test-uid-123/data/latest/")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_url_generation_events(self, mock_request, mock_client):
        """Test URL generation for events endpoint"""
        mock_request.return_value = {"events": []}
        devices_api = DevicesAPI(mock_client)

        with patch.object(devices_api, "_url") as mock_url:
            mock_url.return_value = (
                "https://api.example.com/api/v4/devices/uid/test-uid-123/events/"
            )

            devices_api.get_events_by_uid("test-uid-123")

            mock_url.assert_called_once_with("devices/uid/test-uid-123/events/")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_commands_by_uid_success(
        self, mock_request, mock_client, mock_device_response
    ):
        """Test successful commands retrieval by UID"""
        mock_request.return_value = mock_device_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_commands_by_uid("test-uid-123")

        assert result == mock_device_response
        mock_request.assert_called_once()

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_commands_by_uid_with_filters(
        self, mock_request, mock_client, mock_device_response
    ):
        """Test commands retrieval with filters"""
        mock_request.return_value = mock_device_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_commands_by_uid(
            "test-uid-123", status="sent", limit="5"
        )

        assert result == mock_device_response
        mock_request.assert_called_once_with(
            mock_request.call_args[0][0], params={"status": "sent", "limit": "5"}
        )

    def test_get_commands_by_uid_invalid_uid_type(self, mock_client):
        """Test get_commands_by_uid with invalid UID type"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.get_commands_by_uid(123)

    def test_get_commands_by_uid_empty_uid(self, mock_client):
        """Test get_commands_by_uid with empty UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.get_commands_by_uid("")

    def test_get_commands_by_uid_whitespace_uid(self, mock_client):
        """Test get_commands_by_uid with whitespace-only UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.get_commands_by_uid("   ")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_commands_by_uid_not_found(self, mock_request, mock_client):
        """Test get_commands_by_uid when device not found"""
        mock_request.side_effect = ResourceNotFoundError("Not found")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ResourceNotFoundError, match="Not found"):
            devices_api.get_commands_by_uid("test-uid-123")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_commands_by_uid_unauthorised(self, mock_request, mock_client):
        """Test get_commands_by_uid when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Request not authorised")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(UnauthorisedError, match="Request not authorised"):
            devices_api.get_commands_by_uid("test-uid-123")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_commands_by_uid_forbidden(self, mock_request, mock_client):
        """Test get_commands_by_uid when access forbidden"""
        mock_request.side_effect = PermissionError(
            "You are not authorised to access this resource"
        )
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(
            PermissionError, match="You are not authorised to access this resource"
        ):
            devices_api.get_commands_by_uid("test-uid-123")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_commands_by_uid_server_error(self, mock_request, mock_client):
        """Test get_commands_by_uid with server error"""
        mock_request.side_effect = ConnectAPIError("ERR")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ConnectAPIError, match="ERR"):
            devices_api.get_commands_by_uid("test-uid-123")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_url_generation_commands(self, mock_request, mock_client):
        """Test URL generation for commands endpoint"""
        mock_request.return_value = {"commands": []}
        devices_api = DevicesAPI(mock_client)

        with patch.object(devices_api, "_url") as mock_url:
            mock_url.return_value = (
                "https://api.example.com/api/v4/devices/uid/test-uid-123/commands/"
            )

            devices_api.get_commands_by_uid("test-uid-123")

            mock_url.assert_called_once_with("devices/uid/test-uid-123/commands/")

    @patch("connect_client.mixins.ResourceMixin.make_patch_request")
    def test_move_to_folder_success(self, mock_request, mock_client):
        """Test successful device move to folder by ID"""
        mock_request.return_value = {"success": True}
        devices_api = DevicesAPI(mock_client)

        result = devices_api.move_to_folder(1, 2)

        assert result == {"success": True}
        mock_request.assert_called_once()

    def test_move_to_folder_invalid_device_id(self, mock_client):
        """Test move_to_folder with invalid device ID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.move_to_folder(-1, 2)

    def test_move_to_folder_invalid_folder_id(self, mock_client):
        """Test move_to_folder with invalid folder ID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.move_to_folder(1, 0)

    @patch("connect_client.mixins.ResourceMixin.make_patch_request")
    def test_move_to_folder_by_uid_success(self, mock_request, mock_client):
        """Test successful device move to folder by UID"""
        mock_request.return_value = {"success": True}
        devices_api = DevicesAPI(mock_client)

        result = devices_api.move_to_folder_by_uid("test-uid-123", 2)

        assert result == {"success": True}
        mock_request.assert_called_once()

    def test_move_to_folder_by_uid_invalid_uid(self, mock_client):
        """Test move_to_folder_by_uid with invalid UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.move_to_folder_by_uid("", 2)

    def test_move_to_folder_by_uid_invalid_folder_id(self, mock_client):
        """Test move_to_folder_by_uid with invalid folder ID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.move_to_folder_by_uid("test-uid-123", -1)

    @patch("connect_client.mixins.ResourceMixin.make_patch_request")
    def test_set_lifecycle_success(self, mock_request, mock_client):
        """Test successful lifecycle state change by ID"""
        mock_request.return_value = {"state": 2}
        devices_api = DevicesAPI(mock_client)

        result = devices_api.set_lifecycle(1, 2)

        assert result == {"state": 2}
        mock_request.assert_called_once()

    def test_set_lifecycle_invalid_device_id(self, mock_client):
        """Test set_lifecycle with invalid device ID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.set_lifecycle("invalid", 2)

    def test_set_lifecycle_invalid_state(self, mock_client):
        """Test set_lifecycle with invalid target state"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.set_lifecycle(1, -1)

    @patch("connect_client.mixins.ResourceMixin.make_patch_request")
    def test_set_lifecycle_by_uid_success(self, mock_request, mock_client):
        """Test successful lifecycle state change by UID"""
        mock_request.return_value = {"state": 2}
        devices_api = DevicesAPI(mock_client)

        result = devices_api.set_lifecycle_by_uid("test-uid-123", 2)

        assert result == {"state": 2}
        mock_request.assert_called_once()

    def test_set_lifecycle_by_uid_invalid_uid(self, mock_client):
        """Test set_lifecycle_by_uid with invalid UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.set_lifecycle_by_uid(None, 2)

    def test_set_lifecycle_by_uid_invalid_state(self, mock_client):
        """Test set_lifecycle_by_uid with invalid target state"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.set_lifecycle_by_uid("test-uid-123", 0)

    @patch("connect_client.mixins.ResourceMixin.make_post_request")
    def test_issue_command_success(self, mock_request, mock_client):
        """Test successful command issue by ID"""
        mock_request.return_value = {"status": "sent"}
        devices_api = DevicesAPI(mock_client)
        command = {"rpc": "test", "args": [], "pid": "0", "ttl": 300, "qos": 0}

        result = devices_api.issue_command(1, command)

        assert result == {"status": "sent"}
        mock_request.assert_called_once()

    def test_issue_command_invalid_device_id(self, mock_client):
        """Test issue_command with invalid device ID"""
        devices_api = DevicesAPI(mock_client)
        command = {"rpc": "test", "args": [], "pid": "0", "ttl": 300, "qos": 0}

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.issue_command(0, command)

    def test_issue_command_invalid_command_type(self, mock_client):
        """Test issue_command with invalid command type"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="Command must be a dictionary"):
            devices_api.issue_command(1, "invalid")

    def test_issue_command_missing_fields(self, mock_client):
        """Test issue_command with missing command fields"""
        devices_api = DevicesAPI(mock_client)
        command = {"rpc": "test"}

        with pytest.raises(ValueError, match="Command missing required fields"):
            devices_api.issue_command(1, command)

    def test_issue_command_invalid_rpc_type(self, mock_client):
        """Test issue_command with invalid rpc type"""
        devices_api = DevicesAPI(mock_client)
        command = {"rpc": 123, "args": [], "pid": "0", "ttl": 300, "qos": 0}

        with pytest.raises(ValueError, match="Command 'rpc' must be a string"):
            devices_api.issue_command(1, command)

    def test_issue_command_invalid_args_type(self, mock_client):
        """Test issue_command with invalid args type"""
        devices_api = DevicesAPI(mock_client)
        command = {"rpc": "test", "args": "invalid", "pid": "0", "ttl": 300, "qos": 0}

        with pytest.raises(ValueError, match="Command 'args' must be a list"):
            devices_api.issue_command(1, command)

    def test_issue_command_invalid_ttl_negative(self, mock_client):
        """Test issue_command with negative ttl"""
        devices_api = DevicesAPI(mock_client)
        command = {"rpc": "test", "args": [], "pid": "0", "ttl": -1, "qos": 0}

        with pytest.raises(
            ValueError, match="Command 'ttl' must be a non-negative number"
        ):
            devices_api.issue_command(1, command)

    def test_issue_command_invalid_qos_negative(self, mock_client):
        """Test issue_command with negative qos"""
        devices_api = DevicesAPI(mock_client)
        command = {"rpc": "test", "args": [], "pid": "0", "ttl": 300, "qos": -1}

        with pytest.raises(
            ValueError, match="Command 'qos' must be a non-negative integer"
        ):
            devices_api.issue_command(1, command)

    @patch("connect_client.mixins.ResourceMixin.make_post_request")
    def test_issue_command_by_uid_success(self, mock_request, mock_client):
        """Test successful command issue by UID"""
        mock_request.return_value = {"status": "sent"}
        devices_api = DevicesAPI(mock_client)
        command = {"rpc": "test", "args": [], "pid": "0", "ttl": 300, "qos": 0}

        result = devices_api.issue_command_by_uid("test-uid-123", command)

        assert result == {"status": "sent"}
        mock_request.assert_called_once()

    def test_issue_command_by_uid_invalid_uid(self, mock_client):
        """Test issue_command_by_uid with invalid UID"""
        devices_api = DevicesAPI(mock_client)
        command = {"rpc": "test", "args": [], "pid": "0", "ttl": 300, "qos": 0}

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.issue_command_by_uid("   ", command)

    def test_issue_command_by_uid_invalid_command(self, mock_client):
        """Test issue_command_by_uid with invalid command"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="Command must be a dictionary"):
            devices_api.issue_command_by_uid("test-uid-123", [])

    @patch("connect_client.mixins.ResourceMixin.make_patch_request")
    def test_move_to_folder_data_structure(self, mock_request, mock_client):
        """Test move_to_folder sends correct data structure"""
        devices_api = DevicesAPI(mock_client)

        devices_api.move_to_folder(1, 5)

        _, kwargs = mock_request.call_args
        assert kwargs["json"] == {"folder": 5}

    @patch("connect_client.mixins.ResourceMixin.make_patch_request")
    def test_set_lifecycle_data_structure(self, mock_request, mock_client):
        """Test set_lifecycle sends correct data structure"""
        devices_api = DevicesAPI(mock_client)

        devices_api.set_lifecycle(1, 3)

        _, kwargs = mock_request.call_args
        assert kwargs["json"] == {"state": 3}

    @patch("connect_client.mixins.ResourceMixin.make_post_request")
    def test_issue_command_data_structure(self, mock_request, mock_client):
        """Test issue_command sends correct data structure"""
        devices_api = DevicesAPI(mock_client)
        command = {
            "rpc": "reboot",
            "args": ["force"],
            "pid": "123",
            "ttl": 600,
            "qos": 1,
        }

        devices_api.issue_command(1, command)

        _, kwargs = mock_request.call_args
        assert kwargs["json"] == command

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_success(self, mock_request, mock_client):
        """Test successful device list retrieval by folder ID"""
        mock_response = [
            {"id": 1, "uid": "device-1", "name": "Device 1"},
            {"id": 2, "uid": "device-2", "name": "Device 2"},
        ]
        mock_request.return_value = mock_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.list_by_folder(5)

        assert result == mock_response
        mock_request.assert_called_once()

    def test_list_by_folder_invalid_id_type(self, mock_client):
        """Test list_by_folder with invalid folder ID type"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.list_by_folder("invalid")

    def test_list_by_folder_invalid_id_zero(self, mock_client):
        """Test list_by_folder with zero folder ID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.list_by_folder(0)

    def test_list_by_folder_invalid_id_negative(self, mock_client):
        """Test list_by_folder with negative folder ID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.list_by_folder(-1)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_with_filters(self, mock_request, mock_client):
        """Test list_by_folder with filter parameters"""
        mock_response = [{"id": 1, "uid": "device-1", "name": "Device 1"}]
        mock_request.return_value = mock_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.list_by_folder(5, limit="10", offset="0", status="active")

        assert result == mock_response
        mock_request.assert_called_once_with(
            mock_request.call_args[0][0],
            params={"limit": "10", "offset": "0", "status": "active"},
        )

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_empty_result(self, mock_request, mock_client):
        """Test list_by_folder when folder has no devices"""
        mock_request.return_value = []
        devices_api = DevicesAPI(mock_client)

        result = devices_api.list_by_folder(5)

        assert result == []
        mock_request.assert_called_once()

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_not_found(self, mock_request, mock_client):
        """Test list_by_folder when folder not found"""
        mock_request.side_effect = ResourceNotFoundError("Folder not found")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ResourceNotFoundError, match="Folder not found"):
            devices_api.list_by_folder(999)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_unauthorised(self, mock_request, mock_client):
        """Test list_by_folder when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Request not authorised")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(UnauthorisedError, match="Request not authorised"):
            devices_api.list_by_folder(5)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_forbidden(self, mock_request, mock_client):
        """Test list_by_folder when access forbidden"""
        mock_request.side_effect = PermissionError(
            "You are not authorised to access this resource"
        )
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(
            PermissionError, match="You are not authorised to access this resource"
        ):
            devices_api.list_by_folder(5)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_server_error(self, mock_request, mock_client):
        """Test list_by_folder with server error"""
        mock_request.side_effect = ConnectAPIError("Server error")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ConnectAPIError, match="Server error"):
            devices_api.list_by_folder(5)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_url_generation(self, mock_request, mock_client):
        """Test URL generation for list_by_folder endpoint"""
        mock_request.return_value = []
        devices_api = DevicesAPI(mock_client)

        with patch.object(devices_api, "_url") as mock_url:
            mock_url.return_value = (
                "https://api.example.com/api/v4/devices/folder/5/"
            )

            devices_api.list_by_folder(5)

            mock_url.assert_called_once_with("devices/folder/5/")

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_lite_success(self, mock_request, mock_client):
        """Test successful lightweight device list retrieval by folder ID"""
        mock_response = [
            {"id": 1, "uid": "device-1", "name": "Device 1"},
            {"id": 2, "uid": "device-2", "name": "Device 2"},
        ]
        mock_request.return_value = mock_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.list_by_folder_lite(5)

        assert result == mock_response
        mock_request.assert_called_once()

    def test_list_by_folder_lite_invalid_id_type(self, mock_client):
        """Test list_by_folder_lite with invalid folder ID type"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.list_by_folder_lite("invalid")

    def test_list_by_folder_lite_invalid_id_zero(self, mock_client):
        """Test list_by_folder_lite with zero folder ID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.list_by_folder_lite(0)

    def test_list_by_folder_lite_invalid_id_negative(self, mock_client):
        """Test list_by_folder_lite with negative folder ID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.list_by_folder_lite(-1)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_lite_with_filters(self, mock_request, mock_client):
        """Test list_by_folder_lite with filter parameters"""
        mock_response = [{"id": 1, "uid": "device-1", "name": "Device 1"}]
        mock_request.return_value = mock_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.list_by_folder_lite(
            5, limit="10", offset="0", status="active"
        )

        assert result == mock_response
        mock_request.assert_called_once_with(
            mock_request.call_args[0][0],
            params={"limit": "10", "offset": "0", "status": "active"},
        )

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_lite_empty_result(self, mock_request, mock_client):
        """Test list_by_folder_lite when folder has no devices"""
        mock_request.return_value = []
        devices_api = DevicesAPI(mock_client)

        result = devices_api.list_by_folder_lite(5)

        assert result == []
        mock_request.assert_called_once()

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_lite_not_found(self, mock_request, mock_client):
        """Test list_by_folder_lite when folder not found"""
        mock_request.side_effect = ResourceNotFoundError("Folder not found")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ResourceNotFoundError, match="Folder not found"):
            devices_api.list_by_folder_lite(999)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_lite_unauthorised(self, mock_request, mock_client):
        """Test list_by_folder_lite when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Request not authorised")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(UnauthorisedError, match="Request not authorised"):
            devices_api.list_by_folder_lite(5)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_lite_forbidden(self, mock_request, mock_client):
        """Test list_by_folder_lite when access forbidden"""
        mock_request.side_effect = PermissionError(
            "You are not authorised to access this resource"
        )
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(
            PermissionError, match="You are not authorised to access this resource"
        ):
            devices_api.list_by_folder_lite(5)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_lite_server_error(self, mock_request, mock_client):
        """Test list_by_folder_lite with server error"""
        mock_request.side_effect = ConnectAPIError("Server error")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ConnectAPIError, match="Server error"):
            devices_api.list_by_folder_lite(5)

    @patch("connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_lite_url_generation(self, mock_request, mock_client):
        """Test URL generation for list_by_folder_lite endpoint"""
        mock_request.return_value = []
        devices_api = DevicesAPI(mock_client)

        with patch.object(devices_api, "_url") as mock_url:
            mock_url.return_value = (
                "https://api.example.com/api/v4/devices/folder/5/lite/"
            )

            devices_api.list_by_folder_lite(5)

            mock_url.assert_called_once_with("devices/folder/5/lite/")
