# Connect Client for Python

## Getting started

```python
from connect_client import ConnectClient

client = ConnectClient(
    api_version="v4",
    base_url="https://capi.trintel.co.za",
    cache=None,
    credentials={
        "email": "YOUR_API_USER_EMAIL",
        "password": "YOUR_API_USER_PASSWORD"
    })
```