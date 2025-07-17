# Connect Client for Python

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python library for interacting with the Connect API. This library provides a clean, type-safe interface for accessing Connect API endpoints with comprehensive error handling and testing support.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [License](#license)

## Installation

### Requirements

- Python 3.12 or higher
- `requests` library

### Install from source

```bash
git clone https://github.com/trinity-telecomms/connect-client.git
cd connect-client
pip install -e .
```

### Install dependencies

```bash
# Install using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

## Quick Start

```python
from connect_client import ConnectClient

# Initialize the client
client = ConnectClient(
    api_version="v4",
    base_url="https://capi.trintel.co.za",
    cache=None,  # Optional: provide cache implementation
    credentials={
        "email": "YOUR_API_USER_EMAIL",
        "password": "YOUR_API_USER_PASSWORD"
    }
)

# Use the client
company = client.orgs.get_company(1)
print(f"Company: {company['name']}")
```

## Testing

### Running Tests

The library includes comprehensive tests with 100% coverage for core modules.

```bash
# Install test dependencies
uv sync --group test

# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=src/connect_client --cov-report=term-missing

# Run specific test file
python -m pytest tests/modules/orgs/test_orgs_api.py -v

# Run tests with verbose output
python -m pytest -v
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.