from typing import Dict, Any

from connect_client.decorators import handle_exceptions
from connect_client.mixins import ResourceMixin
from connect_client.validators import validate_id, validate_uid, validate_command
from .constants import PATH_MAP


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
        url = self._generate_url("device_by_id", PATH_MAP, device_id=device_id)
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
        url = self._generate_url("device_by_uid", PATH_MAP, device_uid=device_uid)
        return self.make_get_request(url)

    @handle_exceptions
    def get_latest_data_by_uid(self, device_uid: str, **filters: str) -> dict[str, Any]:
        """
        GET latest data for a device by UID.

        :param device_uid: The UID of the device to retrieve
        :return: A Device object as dictionary or error response
        """
        validate_uid(device_uid)
        url = self._generate_url("device_latest_data", PATH_MAP, device_uid=device_uid)
        return self.make_get_request(url, params=filters)

    @handle_exceptions
    def get_events_by_uid(
        self, device_uid: str, **filters: str
    ) -> list[dict[str, Any]]:
        """
        GET events for a device by UID.

        :param device_uid: The UID of the device to retrieve
        :return: A Device object as dictionary or error response
        """
        validate_uid(device_uid)
        url = self._generate_url(
            "device_events_by_uid", PATH_MAP, device_uid=device_uid
        )
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
        url = self._generate_url("list_by_folder", PATH_MAP, folder_id=folder_id)
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
        url = self._generate_url("list_by_folder_lite", PATH_MAP, folder_id=folder_id)
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

        url = self._generate_url("device_by_id", PATH_MAP, device_id=device_id)
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

        url = self._generate_url("device_by_uid", PATH_MAP, device_uid=device_uid)
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

        url = self._generate_url("device_by_id", PATH_MAP, device_id=device_id)
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

        url = self._generate_url("device_by_uid", PATH_MAP, device_uid=device_uid)
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
        url = self._generate_url("issue_command", PATH_MAP, device_id=device_id)
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
        url = self._generate_url(
            "issue_command_by_uid", PATH_MAP, device_uid=device_uid
        )
        data = {
            **command,
        }
        return self.make_post_request(url, json=data)
