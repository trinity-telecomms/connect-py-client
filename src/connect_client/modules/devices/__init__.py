from connect_client.exceptions import ConnectAPIError
from connect_client.mixins import ResourceMixin
from .constants import PATH_MAP


class DevicesAPI(ResourceMixin):
    def get_device(self, device_id: int):
        """
        GET a device by ID.

        :param device_id:
        :return: Device object
        """
        url = self._generate_url("device_by_id", PATH_MAP, device_id=device_id)

        try:
            status, response = self.make_get_request(url)
            return response
        except Exception as e:
            print(e)
            raise ConnectAPIError("Failed to get device from Connect API")

    def get_device_by_uid(self, device_uid: str):
        """
        GET a device by UID.

        :param device_uid:
        :return:
        """
        url = self._generate_url("device_by_uid", PATH_MAP, device_uid=device_uid)

        try:
            status, response = self.make_get_request(url)
            return response
        except Exception as e:
            print(e)
            raise ConnectAPIError("Failed to get device from Connect API")
