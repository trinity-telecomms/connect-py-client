import pytest
import responses
from connect_client import ConnectClient


@pytest.fixture
def mock_client():
    """Mock ConnectClient for testing"""
    return ConnectClient(
        api_version="v4",
        base_url="https://api.example.com",
        cache=None,
        credentials={
            "email": "test@example.com",
            "password": "testpass123"
        }
    )


@pytest.fixture
def mock_client_with_cache():
    """Mock ConnectClient with cache for testing"""
    class MockCache:
        def __init__(self):
            self._cache = {}
        
        def get(self, key):
            return self._cache.get(key)
        
        def set(self, key, value, ttl=None):
            self._cache[key] = value
    
    return ConnectClient(
        api_version="v4",
        base_url="https://api.example.com",
        cache=MockCache(),
        credentials={
            "email": "test@example.com",
            "password": "testpass123"
        }
    )


@pytest.fixture
def mock_auth_response():
    """Mock authentication response"""
    return {
        "token": "test_token_123",
        "user": {
            "id": 1,
            "email": "test@example.com"
        }
    }


@pytest.fixture
def mock_company_response():
    """Mock company response"""
    return {
        "id": 1,
        "name": "Test Company",
        "status": "active",
        "created_at": "2023-01-01T00:00:00Z"
    }


@pytest.fixture
def mock_company_folders_response():
    """Mock company folders response"""
    return [
        {
            "id": 1,
            "name": "Folder 1",
            "company_id": 1,
            "created_at": "2023-01-01T00:00:00Z"
        },
        {
            "id": 2,
            "name": "Folder 2",
            "company_id": 1,
            "created_at": "2023-01-01T00:00:00Z"
        }
    ]