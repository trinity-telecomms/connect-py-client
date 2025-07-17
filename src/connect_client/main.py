from .modules.auth import AuthAPI
from .modules.devices import DevicesAPI
from .modules.orgs import OrgsAPI


class ConnectClient:
    def __init__(self, **config):
        self.api_version = config.get("api_version", "v4")
        self.api_url = f"{config.get("base_url")}/api/{self.api_version}"
        self.cache = config.get("cache")
        self.credentials = config.get("credentials")

        # Resource Classes
        self.auth = AuthAPI(self)
        self.devices = DevicesAPI(self)
        self.orgs = OrgsAPI(self)
