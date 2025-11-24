from typing import Dict, Any

from connect_client.decorators import handle_exceptions
from connect_client.mixins import ResourceMixin
from connect_client.validators import validate_msisdn
from .constants import PATH_MAP


class SimsAPI(ResourceMixin):
    @handle_exceptions
    def get_by_msisdn(self, msisdn: str) -> Dict[str, Any]:
        """
        GET a SIM by MSISDN.

        :param msisdn: The MSISDN of the SIM to retrieve
        :return: A SIM object as dictionary or error response
        :raises ValueError: If msisdn is not a string
        """
        validate_msisdn(msisdn)
        url = self._generate_url("sim_by_msisdn", PATH_MAP, msisdn=msisdn)
        return self.make_get_request(url)

    @handle_exceptions
    def send_sms_command_by_msisdn(self, msisdn: str, command: dict) -> dict[str, Any]:
        """
        Issue an arbitrary command via SMS to a SIM by MSISDN.

        :param msisdn:
        :param command:
        :return:
        """
        pass
        # validate_uid(device_uid)
        # validate_command(command)
        # url = self._generate_url(
        #     "issue_command_by_uid", PATH_MAP, device_uid=device_uid
        # )
        # data = {
        #     **command,
        # }
        # return self.make_post_request(url, json=data)
