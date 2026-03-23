from typing import Dict, Any

from trinity_connect_client.decorators import handle_exceptions
from trinity_connect_client.mixins import ResourceMixin
from trinity_connect_client.models.device import Device
from trinity_connect_client.validators import (
    validate_id,
    validate_uid,
    validate_command,
    validate_device_create_request,
)


class DevicesAPI(ResourceMixin):
    @handle_exceptions
    def get(self, device_id: int) -> Dict[str, Any]:
        """
        GET a device by ID.

        :param device_id: The ID of the device to retrieve
        :return: A Device object as dictionary or error response
        :raises ValueError: If device_id is not a positive integer
        """
        validate_id(device_id)
        url = self._url(f"devices/{device_id}/")
        return self.make_get_request(url)

    @handle_exceptions
    def get_by_uid(self, device_uid: str) -> Dict[str, Any]:
        """
        GET a device by UID.

        :param device_uid: The UID of the device to retrieve
        :return: A Device object as dictionary or error response
        :raises ValueError: If device_uid is not a valid string
        """
        validate_uid(device_uid)
        url = self._url(f"devices/uid/{device_uid}/")
        return self.make_get_request(url)

    @handle_exceptions
    def create(self, device_data: dict) -> Device:
        """
        Create a new device.

        :param device_data: Dictionary containing device creation data
            Required fields:
                - folder (int): Folder ID where device will be created
                - uid (str): Unique Device Identifier (15-20 characters, alphanumeric uppercase)

            Optional fields:
                - name (str): Device name
                - description (str): Device description
                - state (int): Device lifecycle state (default: 50)
                - tpp_id (str): Third Party Platform ID
                - imei (str): International Mobile Equipment Identifier
                - imei2 (str): Secondary IMEI
                - serial_number (str): Device serial number
                - comm_interval_contract (int): Communication interval contract
                - command_model (int): Command model ID
                - data_lens (int): Data lens ID
                - event_lens (int): Event lens ID
                - profile (int): Profile ID
                - category (int): Category ID

        :return: Created device as Device instance
        :raises ValueError: If validation fails (invalid fields, invalid values)
        :raises ResourceNotFoundError: If folder not found (404)
        :raises UnauthorisedError: If authentication fails (401)
        :raises PermissionError: If permission denied (403) or lacks 'Can create devices' role
        :raises ConnectAPIError: If API request fails
        """
        cleaned_data = validate_device_create_request(device_data)

        url = self._url("devices/device/")
        response = self.make_post_request(url, json=cleaned_data)
        return Device.from_dict(response)

    @handle_exceptions
    def get_latest_data_by_uid(self, device_uid: str, **filters: str) -> dict[str, Any]:
        """
        GET latest data for a device by UID.

        :param device_uid: The UID of the device to retrieve
        :return: A Device object as dictionary or error response
        """
        validate_uid(device_uid)
        url = self._url(f"devices/uid/{device_uid}/data/latest/")
        return self.make_get_request(url, params=filters)

    @handle_exceptions
    def get_events_by_uid(
        self, device_uid: str, **filters: str
    ) -> list[dict[str, Any]]:
        """
        GET events for a device by UID.

        :param device_uid: The UID of the device to retrieve
        :return:
        """
        validate_uid(device_uid)
        url = self._url(f"devices/uid/{device_uid}/events/")
        return self.make_get_request(url, params=filters)

    @handle_exceptions
    def get_commands_by_uid(
        self, device_uid: str, **filters: str
    ) -> list[dict[str, Any]]:
        """
        GET commands for a device by UID.

        :param device_uid: The UID of the device to retrieve
        :return:
        """
        validate_uid(device_uid)
        url = self._url(f"devices/uid/{device_uid}/commands/")
        return self.make_get_request(url, params=filters)

    @handle_exceptions
    def list_by_folder(self, folder_id: int, **filters: str) -> list[dict[str, Any]]:
        """
        GET list of devices by folder ID.

        :param folder_id:
        :param filters:
        :return:
        """
        validate_id(folder_id)
        url = self._url(f"devices/folder/{folder_id}/")
        return self.make_get_request(url, params=filters)

    @handle_exceptions
    def list_by_folder_lite(
        self, folder_id: int, **filters: str
    ) -> list[dict[str, Any]]:
        """
        GET lightweight list of devices by folder ID.

        :param folder_id:
        :param filters:
        :return:
        """
        validate_id(folder_id)
        url = self._url(f"devices/folder/{folder_id}/lite/")
        return self.make_get_request(url, params=filters)

    @handle_exceptions
    def move_to_folder(self, device_id: int, folder_id: int) -> dict[str, Any]:
        """
        Move a device identified by ID to a folder identified by ID.

        :param device_id:
        :param folder_id:
        :return:
        """
        validate_id(device_id)
        validate_id(folder_id)

        url = self._url(f"devices/{device_id}/")
        data = {
            "folder": folder_id,
        }
        return self.make_patch_request(url, json=data)

    @handle_exceptions
    def move_to_folder_by_uid(self, device_uid: str, folder_id: int) -> dict[str, Any]:
        """
        Move a device identified by UID to a folder identified by ID.

        :param device_uid:
        :param folder_id:
        :return:
        """
        validate_uid(device_uid)
        validate_id(folder_id)

        url = self._url(f"devices/uid/{device_uid}/")
        data = {
            "folder": folder_id,
        }
        return self.make_patch_request(url, json=data)

    @handle_exceptions
    def set_lifecycle(self, device_id: int, target_state: int) -> dict[str, Any]:
        """
        Change the lifecycle state of a device by ID.

        :param device_id:
        :param target_state:
        :return:
        """
        validate_id(device_id)
        validate_id(target_state)

        url = self._url(f"devices/{device_id}/")
        data = {
            "state": target_state,
        }
        return self.make_patch_request(url, json=data)

    @handle_exceptions
    def set_lifecycle_by_uid(
        self, device_uid: str, target_state: int
    ) -> dict[str, Any]:
        """
        Change the lifecycle state of a device by UID.

        :param device_uid:
        :param target_state:
        :return:
        """
        validate_uid(device_uid)
        validate_id(target_state)

        url = self._url(f"devices/uid/{device_uid}/")
        data = {
            "state": target_state,
        }
        return self.make_patch_request(url, json=data)

    @handle_exceptions
    def issue_command(self, device_id: int, command: dict) -> dict[str, Any]:
        """
        Issue an arbitrary command to a device by ID.

        :param device_id:
        :param command:
        :return:
        """
        validate_id(device_id)
        validate_command(command)
        url = self._url(f"devices/{device_id}/command/send/")
        data = {
            **command,
        }
        return self.make_post_request(url, json=data)

    @handle_exceptions
    def issue_command_by_uid(self, device_uid: str, command: dict) -> dict[str, Any]:
        """
        Issue an arbitrary command to a device by UID.

        :param device_uid:
        :param command:
        :return:
        """
        validate_uid(device_uid)
        validate_command(command)
        url = self._url(f"devices/uid/{device_uid}/command/send/")
        data = {
            **command,
        }
        return self.make_post_request(url, json=data)

    @handle_exceptions
    def issue_stored_command_by_uid(
        self, device_uid: str, command_code: int
    ) -> dict[str, Any]:
        """
        Issue a pre-configured stored command to a device by UID.

        Stored commands are pre-configured automation scripts in Connect,
        referenced by their numeric code — not direct device-level RPCs.

        :param device_uid: The UID of the device
        :param command_code: The numeric stored command code (e.g., 240, 248)
        :return: API response as dictionary
        """
        validate_uid(device_uid)
        validate_id(command_code)
        url = self._url(f"devices/uid/{device_uid}/command/send/stored/")
        data = {"command": command_code}
        return self.make_post_request(url, json=data)

    @handle_exceptions
    def update_by_uid(self, device_uid: str, device_data: dict) -> Device:
        """
        Update (PATCH) specific fields of a device by UID.

        This performs a partial update - only the fields provided will be updated,
        all other fields remain unchanged.

        :param device_uid: The UID of the device to update
        :param device_data: Dictionary containing fields to update
            Updatable fields (all optional):
                - name (str): Device name
                - description (str): Device description
                - state (int): Device lifecycle state
                - tpp_id (str): Third Party Platform ID
                - folder (int): Folder ID to move device to
                - imei (str): International Mobile Equipment Identifier
                - imei2 (str): Secondary IMEI
                - serial_number (str): Device serial number
                - comm_interval_contract (int): Communication interval contract
                - command_model (int): Command model ID
                - data_lens (int): Data lens ID
                - event_lens (int): Event lens ID
                - profile (int): Profile ID
        :return: Updated device as Device instance
        :raises ValueError: If device_uid is not a valid string
        :raises ResourceNotFoundError: If device not found (404)
        :raises UnauthorisedError: If authentication fails (401)
        :raises PermissionError: If permission denied (403)
        :raises ConnectAPIError: If API request fails
        """
        validate_uid(device_uid)
        url = self._url(f"devices/uid/{device_uid}/")
        response = self.make_patch_request(url, json=device_data)
        return Device.from_dict(response)

    @handle_exceptions
    def overwrite_by_uid(self, device_uid: str, device_data: dict) -> Device:
        """
        Overwrite (PUT) all fields of a device by UID.

        This performs a full replacement - all required fields must be provided.
        Fields not included in the request will be set to their default values.

        Required fields:
            - folder (int): Folder ID where device resides
            - uid (str): Unique Device Identifier

        Optional fields (will use defaults if not provided):
            - name (str): Device name
            - description (str): Device description
            - state (int): Device lifecycle state (default: 50)
            - tpp_id (str): Third Party Platform ID
            - imei (str): International Mobile Equipment Identifier
            - imei2 (str): Secondary IMEI
            - serial_number (str): Device serial number
            - comm_interval_contract (int): Communication interval contract
            - command_model (int): Command model ID
            - data_lens (int): Data lens ID
            - event_lens (int): Event lens ID
            - profile (int): Profile ID

        :param device_uid: The UID of the device to overwrite
        :param device_data: Dictionary containing ALL device fields
        :return: Overwritten device as Device instance
        :raises ValueError: If device_uid is not a valid string or validation fails
        :raises ResourceNotFoundError: If device not found (404)
        :raises UnauthorisedError: If authentication fails (401)
        :raises PermissionError: If permission denied (403)
        :raises ConnectAPIError: If API request fails
        """
        validate_uid(device_uid)
        url = self._url(f"devices/uid/{device_uid}/")
        response = self.make_put_request(url, json=device_data)
        return Device.from_dict(response)

    @handle_exceptions
    def delete_by_uid(self, device_uid: str) -> None:
        """
        Delete a device by UID.

        This is a destructive operation that permanently removes the device
        and all associated data. This action is irreversible.

        Consider marking the device as 'Deactivated' or 'Pending Deletion'
        instead for a non-destructive alternative.

        :param device_uid: The UID of the device to delete
        :return: None
        :raises ValueError: If device_uid is not a valid string
        :raises ResourceNotFoundError: If device not found (404)
        :raises UnauthorisedError: If authentication fails (401)
        :raises PermissionError: If permission denied (403)
        :raises ConnectAPIError: If API request fails
        """
        validate_uid(device_uid)
        url = self._url(f"devices/uid/{device_uid}/")
        self.make_delete_request(url)
