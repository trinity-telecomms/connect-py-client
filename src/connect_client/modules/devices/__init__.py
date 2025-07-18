from typing import Dict, Any

from connect_client.exceptions import UnauthorisedError, ResourceNotFoundError
from connect_client.exceptions.error_responses import ErrorResponse
from connect_client.mixins import ResourceMixin
from .constants import PATH_MAP


class DevicesAPI(ResourceMixin):
    def get_device(self, device_id: int) -> Dict[str, Any]:
        """
        GET a device by ID.

        :param device_id: The ID of the device to retrieve
        :return: A Device object as dictionary or error response
        :raises ValueError: If device_id is not a positive integer
        """
        if not isinstance(device_id, int) or device_id <= 0:
            raise ValueError("device_id must be a positive integer")

        url = self._generate_url("device_by_id", PATH_MAP, device_id=device_id)

        try:
            return self.make_get_request(url)
        except UnauthorisedError:
            return ErrorResponse.unauthorised()
        except PermissionError:
            return ErrorResponse.forbidden()
        except ResourceNotFoundError:
            return ErrorResponse.not_found("Device")
        except Exception:
            return ErrorResponse.api_error()

    def get_device_by_uid(self, device_uid: str) -> Dict[str, Any]:
        """
        GET a device by UID.

        :param device_uid: The UID of the device to retrieve
        :return: A Device object as dictionary or error response
        :raises ValueError: If device_uid is not a valid string
        """
        if not isinstance(device_uid, str) or not device_uid.strip():
            raise ValueError("device_uid must be a non-empty string")

        url = self._generate_url("device_by_uid", PATH_MAP, device_uid=device_uid)

        try:
            return self.make_get_request(url)
        except UnauthorisedError:
            return ErrorResponse.unauthorised()
        except PermissionError:
            return ErrorResponse.forbidden()
        except ResourceNotFoundError:
            return ErrorResponse.not_found("Device")
        except Exception:
            return ErrorResponse.api_error()
