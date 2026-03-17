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


@pytest.fixture
def mock_created_device_response():
    """Mock created device response with all required fields"""
    return {
        "id": 1,
        "url": "https://api.example.com/api/v4/devices/1/",
        "name": "",
        "description": "",
        "state": 50,
        "t_type": 1,
        "tpp_id": None,
        "company": 1,
        "folder": 5,
        "state_display": "Created",
        "t_type_display": "Device",
        "company_name": "Test Company",
        "folder_name": "Test Folder",
        "company_url": "https://api.example.com/api/v4/orgs/company/1/",
        "folder_url": "https://api.example.com/api/v4/orgs/folder/5/",
        "aux_values_url": "https://api.example.com/api/v4/devices/1/aux_values/",
        "uid": "123456789012345",
        "imei": "",
        "imei2": "",
        "serial_number": "",
        "comm_interval_contract": 3600,
        "comm_state": 0,
        "comm_state_display": "Unknown",
        "youngest_comm_timestamp": "2023-01-01T00:00:00Z",
        "command_model": 1,
        "data_lens": 1,
        "event_lens": None,
        "profile": None,
        "commands_url": "https://api.example.com/api/v4/devices/1/commands/",
        "latest_data_url": "https://api.example.com/api/v4/devices/1/data/latest/",
        "events_url": "https://api.example.com/api/v4/devices/1/events/",
        "meta_url": "https://api.example.com/api/v4/devices/1/meta/",
        "geo_url": "https://api.example.com/api/v4/devices/1/geo/",
        "category_url": "https://api.example.com/api/v4/devices/1/category/",
        "tags_url": "https://api.example.com/api/v4/devices/1/tags/",
    }
