import pytest
from unittest.mock import patch

from trinity_connect_client.modules.devices import DevicesAPI
from trinity_connect_client.models.device import Device
from trinity_connect_client.exceptions import (
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_not_found(self, mock_request, mock_client):
        """Test get when device not found"""
        mock_request.side_effect = ResourceNotFoundError("Requested resource not found")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ResourceNotFoundError, match="Requested resource not found"):
            devices_api.get(1)

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_unauthorised(self, mock_request, mock_client):
        """Test get when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Request not authorised")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(UnauthorisedError, match="Request not authorised"):
            devices_api.get(1)

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_by_uid_not_found(self, mock_request, mock_client):
        """Test get_by_uid when device not found"""
        mock_request.side_effect = ResourceNotFoundError("Not found")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ResourceNotFoundError, match="Not found"):
            devices_api.get_by_uid("test-uid-123")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_by_uid_unauthorised(self, mock_request, mock_client):
        """Test get_by_uid when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Request not authorised")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(UnauthorisedError, match="Request not authorised"):
            devices_api.get_by_uid("test-uid-123")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_by_uid_server_error(self, mock_request, mock_client):
        """Test get_by_uid with server error"""
        mock_request.side_effect = ConnectAPIError("ERR")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ConnectAPIError, match="ERR"):
            devices_api.get_by_uid("test-uid-123")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_url_generation(self, mock_request, mock_client):
        """Test URL generation for endpoints"""
        mock_request.return_value = {"id": 1}
        devices_api = DevicesAPI(mock_client)

        with patch.object(devices_api, "_url") as mock_url:
            mock_url.return_value = "https://api.example.com/api/v4/devices/1/"

            devices_api.get(1)

            mock_url.assert_called_once_with("devices/1/")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_latest_data_by_uid_success(
        self, mock_request, mock_client, mock_device_response
    ):
        """Test successful latest data retrieval by UID"""
        mock_request.return_value = mock_device_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_latest_data_by_uid("test-uid-123")

        assert result == mock_device_response
        mock_request.assert_called_once()

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_events_by_uid_success(
        self, mock_request, mock_client, mock_device_response
    ):
        """Test successful events retrieval by UID"""
        mock_request.return_value = mock_device_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_events_by_uid("test-uid-123")

        assert result == mock_device_response
        mock_request.assert_called_once()

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_commands_by_uid_success(
        self, mock_request, mock_client, mock_device_response
    ):
        """Test successful commands retrieval by UID"""
        mock_request.return_value = mock_device_response
        devices_api = DevicesAPI(mock_client)

        result = devices_api.get_commands_by_uid("test-uid-123")

        assert result == mock_device_response
        mock_request.assert_called_once()

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_commands_by_uid_not_found(self, mock_request, mock_client):
        """Test get_commands_by_uid when device not found"""
        mock_request.side_effect = ResourceNotFoundError("Not found")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ResourceNotFoundError, match="Not found"):
            devices_api.get_commands_by_uid("test-uid-123")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_commands_by_uid_unauthorised(self, mock_request, mock_client):
        """Test get_commands_by_uid when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Request not authorised")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(UnauthorisedError, match="Request not authorised"):
            devices_api.get_commands_by_uid("test-uid-123")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_get_commands_by_uid_server_error(self, mock_request, mock_client):
        """Test get_commands_by_uid with server error"""
        mock_request.side_effect = ConnectAPIError("ERR")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ConnectAPIError, match="ERR"):
            devices_api.get_commands_by_uid("test-uid-123")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
    def test_move_to_folder_data_structure(self, mock_request, mock_client):
        """Test move_to_folder sends correct data structure"""
        devices_api = DevicesAPI(mock_client)

        devices_api.move_to_folder(1, 5)

        _, kwargs = mock_request.call_args
        assert kwargs["json"] == {"folder": 5}

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
    def test_set_lifecycle_data_structure(self, mock_request, mock_client):
        """Test set_lifecycle sends correct data structure"""
        devices_api = DevicesAPI(mock_client)

        devices_api.set_lifecycle(1, 3)

        _, kwargs = mock_request.call_args
        assert kwargs["json"] == {"state": 3}

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_issue_stored_command_by_uid_success(self, mock_request, mock_client):
        """Test successful stored command issue by UID"""
        mock_request.return_value = {"status": "sent"}
        devices_api = DevicesAPI(mock_client)

        result = devices_api.issue_stored_command_by_uid("test-uid-123", 240)

        assert result == {"status": "sent"}
        mock_request.assert_called_once()

    def test_issue_stored_command_by_uid_invalid_uid(self, mock_client):
        """Test issue_stored_command_by_uid with invalid UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.issue_stored_command_by_uid("", 240)

    def test_issue_stored_command_by_uid_invalid_uid_whitespace(self, mock_client):
        """Test issue_stored_command_by_uid with whitespace UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.issue_stored_command_by_uid("   ", 240)

    def test_issue_stored_command_by_uid_invalid_command_code_type(self, mock_client):
        """Test issue_stored_command_by_uid with invalid command code type"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.issue_stored_command_by_uid("test-uid-123", "invalid")

    def test_issue_stored_command_by_uid_invalid_command_code_zero(self, mock_client):
        """Test issue_stored_command_by_uid with zero command code"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.issue_stored_command_by_uid("test-uid-123", 0)

    def test_issue_stored_command_by_uid_invalid_command_code_negative(
        self, mock_client
    ):
        """Test issue_stored_command_by_uid with negative command code"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.issue_stored_command_by_uid("test-uid-123", -1)

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_issue_stored_command_by_uid_not_found(self, mock_request, mock_client):
        """Test issue_stored_command_by_uid when device not found"""
        mock_request.side_effect = ResourceNotFoundError("Not found")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ResourceNotFoundError, match="Not found"):
            devices_api.issue_stored_command_by_uid("test-uid-123", 240)

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_issue_stored_command_by_uid_unauthorised(self, mock_request, mock_client):
        """Test issue_stored_command_by_uid when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Request not authorised")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(UnauthorisedError, match="Request not authorised"):
            devices_api.issue_stored_command_by_uid("test-uid-123", 240)

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_issue_stored_command_by_uid_forbidden(self, mock_request, mock_client):
        """Test issue_stored_command_by_uid when access forbidden"""
        mock_request.side_effect = PermissionError(
            "You are not authorised to access this resource"
        )
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(
            PermissionError, match="You are not authorised to access this resource"
        ):
            devices_api.issue_stored_command_by_uid("test-uid-123", 240)

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_issue_stored_command_by_uid_server_error(self, mock_request, mock_client):
        """Test issue_stored_command_by_uid with server error"""
        mock_request.side_effect = ConnectAPIError("ERR")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ConnectAPIError, match="ERR"):
            devices_api.issue_stored_command_by_uid("test-uid-123", 240)

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_issue_stored_command_by_uid_url_generation(
        self, mock_request, mock_client
    ):
        """Test URL generation for issue_stored_command_by_uid endpoint"""
        mock_request.return_value = {"status": "sent"}
        devices_api = DevicesAPI(mock_client)

        with patch.object(devices_api, "_url") as mock_url:
            mock_url.return_value = "https://api.example.com/api/v4/devices/uid/test-uid-123/command/send/stored/"

            devices_api.issue_stored_command_by_uid("test-uid-123", 240)

            mock_url.assert_called_once_with(
                "devices/uid/test-uid-123/command/send/stored/"
            )

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_issue_stored_command_by_uid_data_structure(
        self, mock_request, mock_client
    ):
        """Test issue_stored_command_by_uid sends correct data structure"""
        devices_api = DevicesAPI(mock_client)

        devices_api.issue_stored_command_by_uid("test-uid-123", 240)

        _, kwargs = mock_request.call_args
        assert kwargs["json"] == {"command": 240}

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_empty_result(self, mock_request, mock_client):
        """Test list_by_folder when folder has no devices"""
        mock_request.return_value = []
        devices_api = DevicesAPI(mock_client)

        result = devices_api.list_by_folder(5)

        assert result == []
        mock_request.assert_called_once()

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_not_found(self, mock_request, mock_client):
        """Test list_by_folder when folder not found"""
        mock_request.side_effect = ResourceNotFoundError("Folder not found")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ResourceNotFoundError, match="Folder not found"):
            devices_api.list_by_folder(999)

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_unauthorised(self, mock_request, mock_client):
        """Test list_by_folder when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Request not authorised")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(UnauthorisedError, match="Request not authorised"):
            devices_api.list_by_folder(5)

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_server_error(self, mock_request, mock_client):
        """Test list_by_folder with server error"""
        mock_request.side_effect = ConnectAPIError("Server error")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ConnectAPIError, match="Server error"):
            devices_api.list_by_folder(5)

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_url_generation(self, mock_request, mock_client):
        """Test URL generation for list_by_folder endpoint"""
        mock_request.return_value = []
        devices_api = DevicesAPI(mock_client)

        with patch.object(devices_api, "_url") as mock_url:
            mock_url.return_value = "https://api.example.com/api/v4/devices/folder/5/"

            devices_api.list_by_folder(5)

            mock_url.assert_called_once_with("devices/folder/5/")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_lite_empty_result(self, mock_request, mock_client):
        """Test list_by_folder_lite when folder has no devices"""
        mock_request.return_value = []
        devices_api = DevicesAPI(mock_client)

        result = devices_api.list_by_folder_lite(5)

        assert result == []
        mock_request.assert_called_once()

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_lite_not_found(self, mock_request, mock_client):
        """Test list_by_folder_lite when folder not found"""
        mock_request.side_effect = ResourceNotFoundError("Folder not found")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ResourceNotFoundError, match="Folder not found"):
            devices_api.list_by_folder_lite(999)

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_lite_unauthorised(self, mock_request, mock_client):
        """Test list_by_folder_lite when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Request not authorised")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(UnauthorisedError, match="Request not authorised"):
            devices_api.list_by_folder_lite(5)

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
    def test_list_by_folder_lite_server_error(self, mock_request, mock_client):
        """Test list_by_folder_lite with server error"""
        mock_request.side_effect = ConnectAPIError("Server error")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ConnectAPIError, match="Server error"):
            devices_api.list_by_folder_lite(5)

    @patch("trinity_connect_client.mixins.ResourceMixin.make_get_request")
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

    # ==================== Device Creation Tests ====================

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_create_success_minimal(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test successful device creation with minimal required fields"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 5, "uid": "123456789012345"}

        result = devices_api.create(device_data)

        assert isinstance(result, Device)
        assert result.id == 1
        assert result.uid == "123456789012345"
        mock_request.assert_called_once()

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_create_success_with_alphanumeric_uid(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test successful device creation with alphanumeric UID"""
        mock_created_device_response["uid"] = "ABC123456789XYZ"
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 5, "uid": "ABC123456789XYZ"}

        result = devices_api.create(device_data)

        assert isinstance(result, Device)
        assert result.id == 1
        assert result.uid == "ABC123456789XYZ"
        mock_request.assert_called_once()

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_create_success_with_all_fields(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test successful device creation with all fields"""
        mock_created_device_response["uid"] = "ABC123456789012XYZ"
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)
        device_data = {
            "folder": 5,
            "uid": "ABC123456789012XYZ",
            "name": "Test Device",
            "description": "A test device",
            "state": 50,
            "imei": "123456789012345",
            "serial_number": "SN12345",
        }

        result = devices_api.create(device_data)

        assert isinstance(result, Device)
        assert result.id == 1
        assert result.uid == "ABC123456789012XYZ"
        mock_request.assert_called_once()

    def test_create_missing_folder(self, mock_client):
        """Test create with missing folder field"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"uid": "123456789012345"}

        with pytest.raises(ValueError, match="Device creation requires 'folder' field"):
            devices_api.create(device_data)

    def test_create_missing_uid(self, mock_client):
        """Test create with missing uid field"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 1}

        with pytest.raises(ValueError, match="Device creation requires 'uid' field"):
            devices_api.create(device_data)

    def test_create_invalid_uid_not_alphanumeric(self, mock_client):
        """Test create with non-alphanumeric characters in uid"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 1, "uid": "ABC-123-456-789"}

        with pytest.raises(
            ValueError, match="Device 'uid' must contain only alphanumeric characters"
        ):
            devices_api.create(device_data)

    def test_create_invalid_uid_lowercase(self, mock_client):
        """Test create with lowercase letters in uid"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 1, "uid": "abc123456789xyz"}

        with pytest.raises(
            ValueError,
            match="Device 'uid' must contain only uppercase letters and digits",
        ):
            devices_api.create(device_data)

    def test_create_invalid_uid_too_short(self, mock_client):
        """Test create with uid too short"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 1, "uid": "ABC12"}

        with pytest.raises(
            ValueError, match="Device 'uid' must be between 15 and 20 characters"
        ):
            devices_api.create(device_data)

    def test_create_invalid_uid_too_long(self, mock_client):
        """Test create with uid too long"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 1, "uid": "ABCDEFGHIJ1234567890XYZ"}

        with pytest.raises(
            ValueError, match="Device 'uid' must be between 15 and 20 characters"
        ):
            devices_api.create(device_data)

    def test_create_invalid_uid_empty(self, mock_client):
        """Test create with empty uid"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 1, "uid": ""}

        with pytest.raises(ValueError, match="Device 'uid' must be a non-empty string"):
            devices_api.create(device_data)

    def test_create_invalid_uid_whitespace(self, mock_client):
        """Test create with whitespace-only uid"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 1, "uid": "   "}

        with pytest.raises(ValueError, match="Device 'uid' must be a non-empty string"):
            devices_api.create(device_data)

    def test_create_invalid_uid_type(self, mock_client):
        """Test create with non-string uid"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 1, "uid": 123456789012345}

        with pytest.raises(ValueError, match="Device 'uid' must be a string"):
            devices_api.create(device_data)

    def test_create_invalid_folder_type(self, mock_client):
        """Test create with non-integer folder"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": "invalid", "uid": "123456789012345"}

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.create(device_data)

    def test_create_invalid_folder_zero(self, mock_client):
        """Test create with zero folder ID"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 0, "uid": "123456789012345"}

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.create(device_data)

    def test_create_invalid_folder_negative(self, mock_client):
        """Test create with negative folder ID"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": -1, "uid": "123456789012345"}

        with pytest.raises(ValueError, match="ID must be a positive integer"):
            devices_api.create(device_data)

    def test_create_invalid_state(self, mock_client):
        """Test create with invalid state value"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 1, "uid": "123456789012345", "state": 999}

        with pytest.raises(ValueError, match="Invalid device state"):
            devices_api.create(device_data)

    def test_create_invalid_category_id_type(self, mock_client):
        """Test create with invalid category_id type"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 1, "uid": "123456789012345", "category_id": "invalid"}

        with pytest.raises(ValueError, match="Device 'category_id' must be an integer"):
            devices_api.create(device_data)

    def test_create_invalid_category_id_zero(self, mock_client):
        """Test create with zero category_id"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 1, "uid": "123456789012345", "category_id": 0}

        with pytest.raises(
            ValueError, match="Device 'category_id' must be a positive integer"
        ):
            devices_api.create(device_data)

    def test_create_invalid_category_id_negative(self, mock_client):
        """Test create with negative category_id"""
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 1, "uid": "123456789012345", "category_id": -1}

        with pytest.raises(
            ValueError, match="Device 'category_id' must be a positive integer"
        ):
            devices_api.create(device_data)

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_create_valid_category_id(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test create with valid category_id"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 5, "uid": "123456789012345", "category_id": 10}

        result = devices_api.create(device_data)

        assert isinstance(result, Device)
        mock_request.assert_called_once()

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_create_payload_cleaning(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test that unexpected fields are removed from payload"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)
        device_data = {
            "folder": 5,
            "uid": "123456789012345",
            "name": "Test Device",
            "unexpected_field": "should be removed",
            "another_invalid": 123,
        }

        result = devices_api.create(device_data)

        assert isinstance(result, Device)
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        sent_data = call_args[1]["json"]
        assert "unexpected_field" not in sent_data
        assert "another_invalid" not in sent_data
        assert sent_data["folder"] == 5
        assert sent_data["uid"] == "123456789012345"
        assert sent_data["name"] == "Test Device"

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_create_comm_state_ignored(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test that comm_state is removed from payload (not allowed on create)"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)
        device_data = {"folder": 5, "uid": "123456789012345", "comm_state": 1}

        result = devices_api.create(device_data)

        assert isinstance(result, Device)
        call_args = mock_request.call_args
        sent_data = call_args[1]["json"]
        assert "comm_state" not in sent_data

    def test_create_invalid_imei_too_long(self, mock_client):
        """Test create with imei too long"""
        devices_api = DevicesAPI(mock_client)
        device_data = {
            "folder": 1,
            "uid": "123456789012345",
            "imei": "12345678901234567890",
        }

        with pytest.raises(
            ValueError, match="Device 'imei' must not exceed 15 characters"
        ):
            devices_api.create(device_data)

    def test_create_invalid_imei2_too_long(self, mock_client):
        """Test create with imei2 too long"""
        devices_api = DevicesAPI(mock_client)
        device_data = {
            "folder": 1,
            "uid": "123456789012345",
            "imei2": "12345678901234567890",
        }

        with pytest.raises(
            ValueError, match="Device 'imei2' must not exceed 15 characters"
        ):
            devices_api.create(device_data)

    def test_create_invalid_serial_number_too_long(self, mock_client):
        """Test create with serial_number too long"""
        devices_api = DevicesAPI(mock_client)
        device_data = {
            "folder": 1,
            "uid": "123456789012345",
            "serial_number": "1234567890123456789012345678901234567890",
        }

        with pytest.raises(
            ValueError, match="Device 'serial_number' must not exceed 30 characters"
        ):
            devices_api.create(device_data)

    def test_create_invalid_tpp_id_too_long(self, mock_client):
        """Test create with tpp_id too long"""
        devices_api = DevicesAPI(mock_client)
        device_data = {
            "folder": 1,
            "uid": "123456789012345",
            "tpp_id": "1234567890123456789012345678901234567890",
        }

        with pytest.raises(
            ValueError, match="Device 'tpp_id' must not exceed 32 characters"
        ):
            devices_api.create(device_data)

    def test_create_invalid_data_type(self, mock_client):
        """Test create with non-dictionary data"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="Device data must be a dictionary"):
            devices_api.create("invalid")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_create_api_error_duplicate_uid(self, mock_request, mock_client):
        """Test create when UID already exists"""
        mock_request.side_effect = ValueError(
            "Validation error: Device with this UID already exists"
        )
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="Validation error"):
            devices_api.create({"folder": 1, "uid": "123456789012345"})

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_create_api_error_folder_not_found(self, mock_request, mock_client):
        """Test create when folder doesn't exist"""
        mock_request.side_effect = ResourceNotFoundError("Requested resource not found")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ResourceNotFoundError, match="Requested resource not found"):
            devices_api.create({"folder": 999, "uid": "123456789012345"})

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_create_api_error_unauthorised(self, mock_request, mock_client):
        """Test create when authentication fails"""
        mock_request.side_effect = UnauthorisedError("Authorisation failed")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(UnauthorisedError, match="Authorisation failed"):
            devices_api.create({"folder": 1, "uid": "123456789012345"})

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_create_api_error_permission_denied(self, mock_request, mock_client):
        """Test create when user lacks permission"""
        mock_request.side_effect = PermissionError(
            "You are not authorised to access this resource"
        )
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(PermissionError, match="You are not authorised"):
            devices_api.create({"folder": 1, "uid": "123456789012345"})

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_create_api_error_server_error(self, mock_request, mock_client):
        """Test create with server error"""
        mock_request.side_effect = ConnectAPIError(
            "Connect API returned unexpected status code: 500"
        )
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ConnectAPIError, match="unexpected status code"):
            devices_api.create({"folder": 1, "uid": "123456789012345"})

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_create_url_generation(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test URL generation for create endpoint"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)

        with patch.object(devices_api, "_url") as mock_url:
            mock_url.return_value = "https://api.example.com/api/v4/devices/device/"

            devices_api.create({"folder": 1, "uid": "123456789012345"})

            mock_url.assert_called_once_with("devices/device/")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_post_request")
    def test_create_data_structure(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test create sends correct data structure"""
        devices_api = DevicesAPI(mock_client)
        device_data = {
            "folder": 5,
            "uid": "123456789012345",
            "name": "Test Device",
            "description": "A test device",
        }

        mock_request.return_value = mock_created_device_response
        devices_api.create(device_data)

        _, kwargs = mock_request.call_args
        assert kwargs["json"] == device_data

    # ==================== Device Update_by_uid Tests ====================

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
    def test_update_by_uid_success(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test successful device update by UID (PATCH)"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)
        update_data = {"name": "Updated Device", "description": "Updated description"}

        result = devices_api.update_by_uid("TEST123456789ABC", update_data)

        assert isinstance(result, Device)
        mock_request.assert_called_once()

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
    def test_update_by_uid_with_folder(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test update_by_uid with folder change"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)
        update_data = {"folder": 10}

        result = devices_api.update_by_uid("TEST123456789ABC", update_data)

        assert isinstance(result, Device)
        mock_request.assert_called_once()

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
    def test_update_by_uid_with_state(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test update_by_uid with state change"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)
        update_data = {"state": 51}

        result = devices_api.update_by_uid("TEST123456789ABC", update_data)

        assert isinstance(result, Device)
        mock_request.assert_called_once()

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
    def test_update_by_uid_multiple_fields(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test update_by_uid with multiple fields"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)
        update_data = {
            "name": "Updated Name",
            "description": "Updated description",
            "serial_number": "SN98765",
            "folder": 10,
        }

        result = devices_api.update_by_uid("TEST123456789ABC", update_data)

        assert isinstance(result, Device)
        mock_request.assert_called_once()

    def test_update_by_uid_invalid_uid_type(self, mock_client):
        """Test update_by_uid with invalid UID type"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.update_by_uid(123, {"name": "test"})

    def test_update_by_uid_empty_uid(self, mock_client):
        """Test update_by_uid with empty UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.update_by_uid("", {"name": "test"})

    def test_update_by_uid_whitespace_uid(self, mock_client):
        """Test update_by_uid with whitespace-only UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.update_by_uid("   ", {"name": "test"})

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
    def test_update_by_uid_not_found(self, mock_request, mock_client):
        """Test update_by_uid when device not found"""
        mock_request.side_effect = ResourceNotFoundError("Device not found")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ResourceNotFoundError, match="Device not found"):
            devices_api.update_by_uid("NONEXISTENT12345", {"name": "test"})

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
    def test_update_by_uid_unauthorised(self, mock_request, mock_client):
        """Test update_by_uid when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Authorisation failed")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(UnauthorisedError, match="Authorisation failed"):
            devices_api.update_by_uid("TEST123456789ABC", {"name": "test"})

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
    def test_update_by_uid_forbidden(self, mock_request, mock_client):
        """Test update_by_uid when access forbidden"""
        mock_request.side_effect = PermissionError(
            "You are not authorised to access this resource"
        )
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(PermissionError, match="You are not authorised"):
            devices_api.update_by_uid("TEST123456789ABC", {"name": "test"})

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
    def test_update_by_uid_validation_error(self, mock_request, mock_client):
        """Test update_by_uid with validation error from API"""
        mock_request.side_effect = ValueError("Validation error: Invalid state value")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="Validation error"):
            devices_api.update_by_uid("TEST123456789ABC", {"state": 999})

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
    def test_update_by_uid_url_generation(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test URL generation for update_by_uid endpoint"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)

        with patch.object(devices_api, "_url") as mock_url:
            mock_url.return_value = (
                "https://api.example.com/api/v4/devices/uid/TEST123456789ABC/"
            )

            devices_api.update_by_uid("TEST123456789ABC", {"name": "test"})

            mock_url.assert_called_once_with("devices/uid/TEST123456789ABC/")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_patch_request")
    def test_update_by_uid_data_structure(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test update_by_uid sends correct data structure"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)
        update_data = {"name": "Updated", "description": "New description"}

        devices_api.update_by_uid("TEST123456789ABC", update_data)

        _, kwargs = mock_request.call_args
        assert kwargs["json"] == update_data

    # ==================== Device Overwrite_by_uid Tests ====================

    @patch("trinity_connect_client.mixins.ResourceMixin.make_put_request")
    def test_overwrite_by_uid_success(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test successful device overwrite by UID (PUT)"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)
        overwrite_data = {
            "folder": 5,
            "uid": "TEST123456789ABC",
            "name": "Overwritten Device",
        }

        result = devices_api.overwrite_by_uid("TEST123456789ABC", overwrite_data)

        assert isinstance(result, Device)
        mock_request.assert_called_once()

    @patch("trinity_connect_client.mixins.ResourceMixin.make_put_request")
    def test_overwrite_by_uid_minimal_required_fields(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test overwrite_by_uid with minimal required fields"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)
        overwrite_data = {"folder": 5, "uid": "TEST123456789ABC"}

        result = devices_api.overwrite_by_uid("TEST123456789ABC", overwrite_data)

        assert isinstance(result, Device)
        mock_request.assert_called_once()

    @patch("trinity_connect_client.mixins.ResourceMixin.make_put_request")
    def test_overwrite_by_uid_all_fields(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test overwrite_by_uid with all fields"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)
        overwrite_data = {
            "folder": 5,
            "uid": "TEST123456789ABC",
            "name": "Full Overwrite",
            "description": "Complete device data",
            "state": 50,
            "imei": "123456789012345",
            "serial_number": "SN12345",
        }

        result = devices_api.overwrite_by_uid("TEST123456789ABC", overwrite_data)

        assert isinstance(result, Device)
        mock_request.assert_called_once()

    def test_overwrite_by_uid_invalid_uid_type(self, mock_client):
        """Test overwrite_by_uid with invalid UID type"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.overwrite_by_uid(123, {"folder": 1})

    def test_overwrite_by_uid_empty_uid(self, mock_client):
        """Test overwrite_by_uid with empty UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.overwrite_by_uid("", {"folder": 1})

    def test_overwrite_by_uid_whitespace_uid(self, mock_client):
        """Test overwrite_by_uid with whitespace-only UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.overwrite_by_uid("   ", {"folder": 1})

    @patch("trinity_connect_client.mixins.ResourceMixin.make_put_request")
    def test_overwrite_by_uid_not_found(self, mock_request, mock_client):
        """Test overwrite_by_uid when device not found"""
        mock_request.side_effect = ResourceNotFoundError("Device not found")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ResourceNotFoundError, match="Device not found"):
            devices_api.overwrite_by_uid(
                "NONEXISTENT12345", {"folder": 1, "uid": "NONEXISTENT12345"}
            )

    @patch("trinity_connect_client.mixins.ResourceMixin.make_put_request")
    def test_overwrite_by_uid_unauthorised(self, mock_request, mock_client):
        """Test overwrite_by_uid when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Authorisation failed")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(UnauthorisedError, match="Authorisation failed"):
            devices_api.overwrite_by_uid("TEST123456789ABC", {"folder": 1})

    @patch("trinity_connect_client.mixins.ResourceMixin.make_put_request")
    def test_overwrite_by_uid_forbidden(self, mock_request, mock_client):
        """Test overwrite_by_uid when access forbidden"""
        mock_request.side_effect = PermissionError(
            "You are not authorised to access this resource"
        )
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(PermissionError, match="You are not authorised"):
            devices_api.overwrite_by_uid("TEST123456789ABC", {"folder": 1})

    @patch("trinity_connect_client.mixins.ResourceMixin.make_put_request")
    def test_overwrite_by_uid_validation_error(self, mock_request, mock_client):
        """Test overwrite_by_uid with validation error from API"""
        mock_request.side_effect = ValueError("Validation error: folder is required")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="Validation error"):
            devices_api.overwrite_by_uid("TEST123456789ABC", {})

    @patch("trinity_connect_client.mixins.ResourceMixin.make_put_request")
    def test_overwrite_by_uid_url_generation(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test URL generation for overwrite_by_uid endpoint"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)

        with patch.object(devices_api, "_url") as mock_url:
            mock_url.return_value = (
                "https://api.example.com/api/v4/devices/uid/TEST123456789ABC/"
            )

            devices_api.overwrite_by_uid(
                "TEST123456789ABC", {"folder": 5, "uid": "TEST123456789ABC"}
            )

            mock_url.assert_called_once_with("devices/uid/TEST123456789ABC/")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_put_request")
    def test_overwrite_by_uid_data_structure(
        self, mock_request, mock_client, mock_created_device_response
    ):
        """Test overwrite_by_uid sends correct data structure"""
        mock_request.return_value = mock_created_device_response
        devices_api = DevicesAPI(mock_client)
        overwrite_data = {"folder": 5, "uid": "TEST123456789ABC", "name": "Overwritten"}

        devices_api.overwrite_by_uid("TEST123456789ABC", overwrite_data)

        _, kwargs = mock_request.call_args
        assert kwargs["json"] == overwrite_data

    # ==================== Device Delete_by_uid Tests ====================

    @patch("trinity_connect_client.mixins.ResourceMixin.make_delete_request")
    def test_delete_by_uid_success(self, mock_request, mock_client):
        """Test successful device deletion by UID"""
        mock_request.return_value = None
        devices_api = DevicesAPI(mock_client)

        result = devices_api.delete_by_uid("TEST123456789ABC")

        assert result is None
        mock_request.assert_called_once()

    def test_delete_by_uid_invalid_uid_type(self, mock_client):
        """Test delete_by_uid with invalid UID type"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.delete_by_uid(123)

    def test_delete_by_uid_empty_uid(self, mock_client):
        """Test delete_by_uid with empty UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.delete_by_uid("")

    def test_delete_by_uid_whitespace_uid(self, mock_client):
        """Test delete_by_uid with whitespace-only UID"""
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ValueError, match="UID must be a non-empty string"):
            devices_api.delete_by_uid("   ")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_delete_request")
    def test_delete_by_uid_not_found(self, mock_request, mock_client):
        """Test delete_by_uid when device not found"""
        mock_request.side_effect = ResourceNotFoundError("Device not found")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ResourceNotFoundError, match="Device not found"):
            devices_api.delete_by_uid("NONEXISTENT12345")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_delete_request")
    def test_delete_by_uid_unauthorised(self, mock_request, mock_client):
        """Test delete_by_uid when access unauthorised"""
        mock_request.side_effect = UnauthorisedError("Authorisation failed")
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(UnauthorisedError, match="Authorisation failed"):
            devices_api.delete_by_uid("TEST123456789ABC")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_delete_request")
    def test_delete_by_uid_forbidden(self, mock_request, mock_client):
        """Test delete_by_uid when access forbidden"""
        mock_request.side_effect = PermissionError(
            "You are not authorised to access this resource"
        )
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(PermissionError, match="You are not authorised"):
            devices_api.delete_by_uid("TEST123456789ABC")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_delete_request")
    def test_delete_by_uid_url_generation(self, mock_request, mock_client):
        """Test URL generation for delete_by_uid endpoint"""
        mock_request.return_value = None
        devices_api = DevicesAPI(mock_client)

        with patch.object(devices_api, "_url") as mock_url:
            mock_url.return_value = (
                "https://api.example.com/api/v4/devices/uid/TEST123456789ABC/"
            )

            devices_api.delete_by_uid("TEST123456789ABC")

            mock_url.assert_called_once_with("devices/uid/TEST123456789ABC/")

    @patch("trinity_connect_client.mixins.ResourceMixin.make_delete_request")
    def test_delete_by_uid_server_error(self, mock_request, mock_client):
        """Test delete_by_uid with server error"""
        mock_request.side_effect = ConnectAPIError(
            "Connect API returned unexpected status code: 500"
        )
        devices_api = DevicesAPI(mock_client)

        with pytest.raises(ConnectAPIError, match="unexpected status code"):
            devices_api.delete_by_uid("TEST123456789ABC")
