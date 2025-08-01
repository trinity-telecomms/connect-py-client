# Connect Client Library

A Python client library for interacting with the Trinity IoT Connect API.

## Installation

Using `uv`:

```bash
uv add git+https://github.com/trinity-telecomms/connect-py-client@v0.1.5
```

Using `pip` with `uv`:

```bash
uv pip install git+https://github.com/trinity-telecomms/connect-py-client@v0.1.5
```

Using `pip`:

```bash
pip install git+https://github.com/trinity-telecomms/connect-py-client@v0.1.5
```

## Quick Start

```python
from connect_client import ConnectClient

# Initialise the client
client = ConnectClient(
    base_url="https://your-connect-api.com",
    credentials={
        "email": "your-email@example.com",
        "password": "your-password"
    }
)

# Get a device by ID
device = client.devices.get(device_id=123)
```

### Additional Resources

- [Error Handling](#error-handling)

## Error Handling

The library includes comprehensive error handling with specific exception types.

### Exception Types

```python
from connect_client.exceptions import (
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
    base_url="https://api.connect.com",  # Required: API base URL
    api_version="v4",  # Optional: API version (default: v4)
    credentials={  # Required for authentication
        "email": "user@example.com",
        "password": "password"
    },
    cache=cache_instance  # Optional: Cache implementation
)
```

---

## Version Information

Current version: **0.1.5**

For more information, visit
the [GitHub repository](https://github.com/trinity-telecomms/connect-py-client).