from typing import Dict, Any

from connect_client.decorators import handle_exceptions
from connect_client.mixins import ResourceMixin
from connect_client.validators import validate_id, validate_uid
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
