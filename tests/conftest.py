import pytest
from trinity_connect_client import ConnectClient


@pytest.fixture
def mock_client():
    """Mock ConnectClient for testing"""
    return ConnectClient(
        api_version="v4",
        base_url="https://api.example.com",
        token="test_service_account_token_123",
    )


@pytest.fixture
def mock_company_response():
    """Mock company response"""
    return {
        "id": 1,
        "name": "Test Company",
        "status": "active",
        "created_at": "2023-01-01T00:00:00Z",
    }


@pytest.fixture
def mock_company_folders_response():
    """Mock company folders response"""
    return [
        {
            "id": 1,
            "name": "Folder 1",
            "company_id": 1,
            "created_at": "2023-01-01T00:00:00Z",
        },
        {
            "id": 2,
            "name": "Folder 2",
            "company_id": 1,
            "created_at": "2023-01-01T00:00:00Z",
        },
    ]


@pytest.fixture
def mock_device_response():
    """Mock device response"""
    return {
        "id": 1,
        "uid": "test-uid-123",
        "name": "Test Device",
        "status": "active",
        "type": "sensor",
        "created_at": "2023-01-01T00:00:00Z",
    }
