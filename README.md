# Connect Client for Python

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python library for interacting with the Trinity IoT Connect API. 
This library provides a clean interface for accessing the Connect API endpoints 
with comprehensive error handling, type hints, and good test coverage.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Using uv (recommended)

```bash
uv add git+https://github.com/trinity-telecomms/connect-py-client@v0.1.8
```

### Using pip

```bash
pip install git+https://github.com/trinity-telecomms/connect-py-client@v0.1.8
```

## Quick Start

```python
from connect_client import ConnectClient
from connect_client.exceptions import ResourceNotFoundError, UnauthorisedError

# Initialize the client
client = ConnectClient(
  api_version="v4",
  base_url="https://capi.trintel.co.za",
  credentials={
      "email": "your-email@example.com",
      "password": "your-password"
  }
)

# Get a device by ID
try:
    device = client.devices.get(device_id=123)
    print(f"Device name: {device['name']}")
except ResourceNotFoundError:
    print("Device not found")
except UnauthorisedError:
    print("Access denied")
```

## Configuration

### Environment Variables

You can set credentials via environment variables:

```bash
export CONNECT_API_EMAIL="your-email@example.com"
export CONNECT_API_PASSWORD="your-password"
export CONNECT_API_BASE_URL="https://capi.trintel.co.za"
```

```python
import os
from connect_client import ConnectClient

client = ConnectClient(
    api_version="v4",
    base_url=os.getenv("CONNECT_API_BASE_URL"),
    credentials={
        "email": os.getenv("CONNECT_API_EMAIL"),
        "password": os.getenv("CONNECT_API_PASSWORD")
    }
)
```

## Error Handling

The library raises specific exceptions for different error conditions:

```python
from connect_client.exceptions import (
    ResourceNotFoundError,
    UnauthorisedError,
    ConnectAPIError
)

try:
    device = client.devices.get(device_id=123)
except ResourceNotFoundError:
    print("Device not found (404)")
except UnauthorisedError:
    print("Authentication failed (401)")
except PermissionError:
    print("Access forbidden (403)")
except ConnectAPIError as e:
    print(f"API error: {e}")
except ValueError as e:
    print(f"Invalid input: {e}")
```

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/trinity-telecomms/connect-py-client.git
cd connect-py-client

# Install dependencies with uv
uv sync

# Run tests
uv run pytest

# Run linting
uv run ruff check .
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=connect_client

# Run specific test file
uv run pytest tests/modules/devices/test_devices_api.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`uv run pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT Licence - 
see the [LICENCE](LICENSE) file for details.