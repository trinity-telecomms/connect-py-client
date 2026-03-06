# Connect Client Library

A Python client library for interacting with the Trinity IoT Connect API.

## Installation

### From PyPI (Recommended)

Using `uv`:

```bash
uv add trinity-connect-client
```

Using `pip`:

```bash
pip install trinity-connect-client
```

### From GitHub

Using `uv`:

```bash
# Install latest release
uv add git+https://github.com/trinity-telecomms/connect-py-client

# Install specific version
uv add git+https://github.com/trinity-telecomms/connect-py-client@v0.2.1
```

Using `pip`:

```bash
# Install latest release
pip install git+https://github.com/trinity-telecomms/connect-py-client

# Install specific version
pip install git+https://github.com/trinity-telecomms/connect-py-client@v0.2.1
```

## Quick Start

```python
from trinity_connect_client import ConnectClient

# Initialise the client
client = ConnectClient(
    base_url="https://capi.trintel.co.za",
    token="your-service-account-token"
)

# Get a device by ID
device = client.devices.get(device_id=123)
```

---

## Device Commands

The library supports sending commands to devices:

### Custom Commands

Send custom RPC commands directly:

```python
command = {
    "rpc": "reboot",
    "args": ["force"],
    "pid": "0",
    "ttl": 300,
    "qos": 0
}
response = client.devices.issue_command_by_uid("device-uid-123", command)
```

### Stored Commands

Issue pre-configured stored commands by their numeric code:

```python
# With default parameters (ttl=60, pid="0")
response = client.devices.issue_stored_command_by_uid(
    device_uid="device-uid-123",
    command_code=240
)

# With custom parameters
response = client.devices.issue_stored_command_by_uid(
    device_uid="device-uid-123",
    command_code=248,
    ttl=120,
    pid="123"
)
```

Stored commands are pre-configured automation scripts in Connect, referenced by numeric codes (e.g., 240, 248).

---

### Additional Resources

- [Error Handling](#error-handling)

## Error Handling

The library includes comprehensive error handling with specific exception types.

### Exception Types

```python
from trinity_connect_client.exceptions import (
    ConnectAPIError,
    ResourceNotFoundError,
    UnauthorisedError
)

try:
    device = client.devices.get(device_id=999999)
except ResourceNotFoundError:
    print("Device not found")
except UnauthorisedError:
    print("Authentication required or token expired")
except ConnectAPIError as e:
    print(f"API Error: {e}")
except ValueError as e:
    print(f"Validation Error: {e}")
```

### Input Validation

The library automatically validates inputs:

```python
# These will raise ValueError exceptions
client.devices.get(device_id=0)  # ID must be positive
client.devices.get_by_uid("")  # UID cannot be empty
client.devices.move_to_folder(-1, 5)  # Device ID must be positive
```

---

## Configuration Options

### Client Configuration

```python
client = ConnectClient(
    base_url="https://capi.trintel.co.za",  # Required: API base URL
    api_version="v4",  # Optional: API version (default: v4)
    token="your-service-account-token"  # Required: Service account token
)
```

---

## Version Information

Current version: **0.3.0**

For more information, visit
the [GitHub repository](https://github.com/trinity-telecomms/connect-py-client).