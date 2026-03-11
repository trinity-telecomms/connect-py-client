# Profile and Customization Resources Implementation Plan

**Date**: 2026-03-06  
**Status**: Ready for Implementation  
**Priority**: High  
**Estimated Effort**: 12-16 hours

---

## Executive Summary

Implement fluent pattern support for **Profile** and **Customization** resources in the Organizations module. These are company-level singleton resources (one instance per company) with GET and UPDATE operations.

### Key Findings from API Exploration

✅ **Profile Resource**
- Endpoint: `/api/v4/orgs/profile/{company_id}/`
- Type: Singleton (one per company)
- Methods: GET, PATCH
- 11 fields including phone, description, API token, settings

✅ **Customization Resource**
- Endpoint: `/api/v4/adaptations/customization/{company_id}/`
- Type: Singleton (one per company)
- Methods: GET, PUT, PATCH
- 17 fields for company feature flags and defaults

---

## API Structure Analysis

### Profile Resource

**Endpoint Pattern**: `/api/v4/orgs/profile/{company_id}/`

**Response Structure**:
```json
{
  "company": 526,
  "url": "http://127.0.0.1:8000/api/v4/orgs/profile/526/",
  "phone": "0123456789",
  "acct_code": "TRIN001",
  "month_start_day": 2,
  "mqtt_cid": "01020000",
  "description": "Company description...",
  "active_tenant_seeker": false,
  "api_token": "1FE6198E-D7C5-11EA-8184-8679137E53B6",
  "max_api_hits": 3000,
  "external_ref": null
}
```

**Supported HTTP Methods**:
- ✅ **GET** - Retrieve profile
- ✅ **PATCH** - Partial update
- ✅ **OPTIONS** - Metadata
- ❌ POST - Not allowed (singleton, no creation)
- ❌ PUT - Not allowed
- ❌ DELETE - Not allowed (cannot delete profile)

**Field Types**:
```python
company: int                    # Company ID (read-only)
url: str                        # Profile URL (read-only)
phone: str                      # Phone number
acct_code: str                  # Account code
month_start_day: int            # Billing cycle start day (1-28)
mqtt_cid: str                   # MQTT client ID
description: str                # Company description
active_tenant_seeker: bool      # Feature flag
api_token: str                  # API token (read-only?)
max_api_hits: int               # API rate limit
external_ref: Optional[str]      # External reference
```

### Customization Resource

**Endpoint Pattern**: `/api/v4/adaptations/customization/{company_id}/`

**Response Structure**:
```json
{
  "url": "http://127.0.0.1:8000/api/v4/adaptations/customization/526/",
  "company": 526,
  "company_url": "http://127.0.0.1:8000/api/v4/orgs/company/526/",
  "suppress_pod": false,
  "list_land_default": 3,
  "has_sims_enabled": true,
  "has_devices_enabled": true,
  "has_device_uptime_report_enabled": false,
  "prominent_sim_field": "msisdn",
  "prominent_device_field": "uid",
  "has_event_notifications_enabled": true,
  "ignore_global_visible_items": false,
  "allow_sim_immunization": true,
  "allow_own_sim_provisioning": false,
  "allow_insecure_mqtt_reg": false,
  "default_device_pdr": 1740,
  "default_device_kai": 990
}
```

**Supported HTTP Methods**:
- ✅ **GET** - Retrieve customization
- ✅ **PUT** - Full update (all fields required)
- ✅ **PATCH** - Partial update
- ✅ **OPTIONS** - Metadata
- ❌ POST - Not allowed (singleton, no creation)
- ❌ DELETE - Not allowed (cannot delete customization)

**Field Types**:
```python
url: str                                    # Customization URL (read-only)
company: int                                # Company ID (read-only)
company_url: str                            # Company URL (read-only)
suppress_pod: bool                          # Feature flag
list_land_default: int                      # Default landing page
has_sims_enabled: bool                      # SIMs module enabled
has_devices_enabled: bool                   # Devices module enabled
has_device_uptime_report_enabled: bool      # Uptime reports enabled
prominent_sim_field: str                    # Primary SIM field to display
prominent_device_field: str                 # Primary device field to display
has_event_notifications_enabled: bool       # Event notifications enabled
ignore_global_visible_items: bool           # Visibility setting
allow_sim_immunization: bool                # SIM immunization allowed
allow_own_sim_provisioning: bool            # Self-provisioning allowed
allow_insecure_mqtt_reg: bool               # Insecure MQTT allowed
default_device_pdr: int                     # Default device PDR
default_device_kai: int                     # Default device KAI
```

---

## Implementation Plan

### Phase 1: Create Models (2-3 hours)

#### 1.1 Create Profile Model

**File**: `src/trinity_connect_client/models/org.py` (extend existing)

```python
@dataclass
class Profile(BaseModel):
    """Represents a company profile from the Connect API."""
    
    company: int
    url: str
    phone: str
    acct_code: str
    month_start_day: int
    mqtt_cid: str
    description: str
    active_tenant_seeker: bool
    api_token: str
    max_api_hits: int
    external_ref: Optional[str]
    
    _client: Optional[Any] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], client: Optional[Any] = None) -> "Profile":
        """
        Create a Profile instance from a dictionary.
        
        :param data: Dictionary containing profile data
        :param client: Optional client for making additional requests
        :return: Profile instance
        """
        instance = cls(
            company=data["company"],
            url=data["url"],
            phone=data["phone"],
            acct_code=data["acct_code"],
            month_start_day=data["month_start_day"],
            mqtt_cid=data["mqtt_cid"],
            description=data["description"],
            active_tenant_seeker=data["active_tenant_seeker"],
            api_token=data["api_token"],
            max_api_hits=data["max_api_hits"],
            external_ref=data.get("external_ref"),
        )
        instance._client = client
        return instance
    
    def update(self, **kwargs) -> "Profile":
        """
        Update profile fields.
        
        :param kwargs: Fields to update
        :return: Updated Profile instance
        :raises RuntimeError: If client is not available
        """
        if self._client is None:
            raise RuntimeError("Client not available on this model instance")
        
        url = self.url
        data = self._client._make_request("PATCH", url, json=kwargs)
        return Profile.from_dict(data, client=self._client)
```

#### 1.2 Create Customization Model

**File**: `src/trinity_connect_client/models/org.py` (extend existing)

```python
@dataclass
class Customization(BaseModel):
    """Represents company customization settings from the Connect API."""
    
    url: str
    company: int
    company_url: str
    suppress_pod: bool
    list_land_default: int
    has_sims_enabled: bool
    has_devices_enabled: bool
    has_device_uptime_report_enabled: bool
    prominent_sim_field: str
    prominent_device_field: str
    has_event_notifications_enabled: bool
    ignore_global_visible_items: bool
    allow_sim_immunization: bool
    allow_own_sim_provisioning: bool
    allow_insecure_mqtt_reg: bool
    default_device_pdr: int
    default_device_kai: int
    
    _client: Optional[Any] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], client: Optional[Any] = None) -> "Customization":
        """
        Create a Customization instance from a dictionary.
        
        :param data: Dictionary containing customization data
        :param client: Optional client for making additional requests
        :return: Customization instance
        """
        instance = cls(
            url=data["url"],
            company=data["company"],
            company_url=data["company_url"],
            suppress_pod=data["suppress_pod"],
            list_land_default=data["list_land_default"],
            has_sims_enabled=data["has_sims_enabled"],
            has_devices_enabled=data["has_devices_enabled"],
            has_device_uptime_report_enabled=data["has_device_uptime_report_enabled"],
            prominent_sim_field=data["prominent_sim_field"],
            prominent_device_field=data["prominent_device_field"],
            has_event_notifications_enabled=data["has_event_notifications_enabled"],
            ignore_global_visible_items=data["ignore_global_visible_items"],
            allow_sim_immunization=data["allow_sim_immunization"],
            allow_own_sim_provisioning=data["allow_own_sim_provisioning"],
            allow_insecure_mqtt_reg=data["allow_insecure_mqtt_reg"],
            default_device_pdr=data["default_device_pdr"],
            default_device_kai=data["default_device_kai"],
        )
        instance._client = client
        return instance
    
    def update(self, **kwargs) -> "Customization":
        """
        Partially update customization fields.
        
        :param kwargs: Fields to update
        :return: Updated Customization instance
        :raises RuntimeError: If client is not available
        """
        if self._client is None:
            raise RuntimeError("Client not available on this model instance")
        
        url = self.url
        data = self._client._make_request("PATCH", url, json=kwargs)
        return Customization.from_dict(data, client=self._client)
    
    def replace(self, **kwargs) -> "Customization":
        """
        Fully replace customization (PUT method).
        
        :param kwargs: All fields for replacement
        :return: Updated Customization instance
        :raises RuntimeError: If client is not available
        """
        if self._client is None:
            raise RuntimeError("Client not available on this model instance")
        
        url = self.url
        data = self._client._make_request("PUT", url, json=kwargs)
        return Customization.from_dict(data, client=self._client)
```

#### 1.3 Update Model Exports

**File**: `src/trinity_connect_client/models/__init__.py`

```python
from .org import Company, Folder, Profile, Customization

__all__ = [
    "Company",
    "Folder",
    "Profile",
    "Customization",
    # ... existing exports
]
```

---

### Phase 2: Enhance Client for Multiple HTTP Methods (1 hour)

**File**: `src/trinity_connect_client/main.py`

Update `_make_request()` to support all HTTP methods:

```python
def _make_request(
    self, 
    method: str, 
    url: str, 
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Make an authenticated request to the Connect API.
    
    :param method: HTTP method (GET, POST, PUT, PATCH, DELETE)
    :param url: Full URL to request
    :param params: Query parameters
    :param json: JSON body for POST/PUT/PATCH requests
    :return: Parsed JSON response
    """
    request_headers = self._get_auth_headers()
    
    try:
        response = requests.request(
            method=method,
            url=url, 
            headers=request_headers, 
            params=params,
            json=json
        )
    except Exception:
        raise ConnectAPIError("Failed to make request to Connect API")
    
    if response.status_code == 401:
        raise UnauthorisedError("Authorisation failed")
    if response.status_code == 403:
        raise PermissionError("You are not authorised to access this resource")
    if response.status_code == 404:
        raise ResourceNotFoundError("Requested resource not found")
    if response.status_code not in [200, 201, 204]:
        raise ConnectAPIError(f"Connect API returned unexpected status code: {response.status_code}")
    
    # Handle empty responses (204 No Content)
    if response.status_code == 204:
        return None
    
    return response.json()
```

---

### Phase 3: Add Properties to Company Model (1 hour)

**File**: `src/trinity_connect_client/models/org.py`

Add fluent properties to Company model:

```python
@dataclass
class Company(BaseModel):
    # ... existing fields ...
    
    @property
    def profile(self) -> Profile:
        """
        Get the company profile.
        
        :return: Profile instance
        :raises RuntimeError: If client is not available
        """
        if self._client is None:
            raise RuntimeError("Client not available on this model instance")
        
        url = f"{self._client.api_url}/orgs/profile/{self.id}/"
        data = self._client._make_request("GET", url)
        return Profile.from_dict(data, client=self._client)
    
    @property
    def customization(self) -> Customization:
        """
        Get the company customization settings.
        
        :return: Customization instance
        :raises RuntimeError: If client is not available
        """
        if self._client is None:
            raise RuntimeError("Client not available on this model instance")
        
        url = f"{self._client.api_url}/adaptations/customization/{self.id}/"
        data = self._client._make_request("GET", url)
        return Customization.from_dict(data, client=self._client)
```

**Note**: Unlike `folders` which returns a query builder, these return the actual model instances directly because they are singleton resources.

---

### Phase 4: Testing (4-5 hours)

#### 4.1 Create Mock Fixtures

**File**: `tests/conftest.py` (extend existing)

```python
@pytest.fixture
def mock_profile_response():
    """Mock profile response"""
    return {
        "company": 526,
        "url": "http://127.0.0.1:8000/api/v4/orgs/profile/526/",
        "phone": "0123456789",
        "acct_code": "TRIN001",
        "month_start_day": 2,
        "mqtt_cid": "01020000",
        "description": "Test company description",
        "active_tenant_seeker": False,
        "api_token": "1FE6198E-D7C5-11EA-8184-8679137E53B6",
        "max_api_hits": 3000,
        "external_ref": None,
    }

@pytest.fixture
def mock_customization_response():
    """Mock customization response"""
    return {
        "url": "http://127.0.0.1:8000/api/v4/adaptations/customization/526/",
        "company": 526,
        "company_url": "http://127.0.0.1:8000/api/v4/orgs/company/526/",
        "suppress_pod": False,
        "list_land_default": 3,
        "has_sims_enabled": True,
        "has_devices_enabled": True,
        "has_device_uptime_report_enabled": False,
        "prominent_sim_field": "msisdn",
        "prominent_device_field": "uid",
        "has_event_notifications_enabled": True,
        "ignore_global_visible_items": False,
        "allow_sim_immunization": True,
        "allow_own_sim_provisioning": False,
        "allow_insecure_mqtt_reg": False,
        "default_device_pdr": 1740,
        "default_device_kai": 990,
    }
```

#### 4.2 Create Test Classes

**File**: `tests/modules/orgs/test_orgs_api.py` (extend existing)

```python
class TestCompanyProfile:
    """Test suite for Company.profile property"""
    
    @patch.object(ConnectClient, "_make_request")
    def test_profile_returns_profile_object(
        self, mock_request, mock_client, mock_company_response, mock_profile_response
    ):
        """Test that profile property returns Profile instance"""
        mock_request.side_effect = [mock_company_response, mock_profile_response]
        
        company = mock_client.orgs.get(526)
        profile = company.profile
        
        assert isinstance(profile, Profile)
        assert profile.company == 526
        assert profile.phone == "0123456789"
        assert profile.acct_code == "TRIN001"
        
        # Verify correct endpoint was called
        assert mock_request.call_count == 2
        args, _ = mock_request.call_args
        assert args[0] == "GET"
        assert args[1] == "http://127.0.0.1:8000/api/v4/orgs/profile/526/"
    
    @patch.object(ConnectClient, "_make_request")
    def test_profile_update(
        self, mock_request, mock_client, mock_company_response, mock_profile_response
    ):
        """Test updating profile fields"""
        updated_response = {**mock_profile_response, "phone": "9999999999"}
        mock_request.side_effect = [
            mock_company_response, 
            mock_profile_response,
            updated_response
        ]
        
        company = mock_client.orgs.get(526)
        profile = company.profile
        updated = profile.update(phone="9999999999")
        
        assert isinstance(updated, Profile)
        assert updated.phone == "9999999999"
        
        # Verify PATCH was called
        args, kwargs = mock_request.call_args
        assert args[0] == "PATCH"
        assert kwargs.get("json") == {"phone": "9999999999"}
    
    def test_profile_without_client_raises_error(self, mock_client, mock_company_response):
        """Test that accessing profile without client raises error"""
        with patch.object(ConnectClient, "_make_request") as mock_request:
            mock_request.return_value = mock_company_response
            
            company = mock_client.orgs.get(526)
            # Simulate no client
            company._client = None
            
            with pytest.raises(RuntimeError, match="Client not available"):
                _ = company.profile


class TestCompanyCustomization:
    """Test suite for Company.customization property"""
    
    @patch.object(ConnectClient, "_make_request")
    def test_customization_returns_customization_object(
        self, mock_request, mock_client, mock_company_response, mock_customization_response
    ):
        """Test that customization property returns Customization instance"""
        mock_request.side_effect = [mock_company_response, mock_customization_response]
        
        company = mock_client.orgs.get(526)
        customization = company.customization
        
        assert isinstance(customization, Customization)
        assert customization.company == 526
        assert customization.has_sims_enabled is True
        assert customization.prominent_device_field == "uid"
        
        # Verify correct endpoint was called
        args, _ = mock_request.call_args
        assert args[0] == "GET"
        assert args[1] == "http://127.0.0.1:8000/api/v4/adaptations/customization/526/"
    
    @patch.object(ConnectClient, "_make_request")
    def test_customization_patch_update(
        self, mock_request, mock_client, mock_company_response, mock_customization_response
    ):
        """Test partial update of customization"""
        updated_response = {**mock_customization_response, "has_sims_enabled": False}
        mock_request.side_effect = [
            mock_company_response,
            mock_customization_response,
            updated_response
        ]
        
        company = mock_client.orgs.get(526)
        customization = company.customization
        updated = customization.update(has_sims_enabled=False)
        
        assert isinstance(updated, Customization)
        assert updated.has_sims_enabled is False
        
        # Verify PATCH was called
        args, kwargs = mock_request.call_args
        assert args[0] == "PATCH"
        assert kwargs.get("json") == {"has_sims_enabled": False}
    
    @patch.object(ConnectClient, "_make_request")
    def test_customization_put_replace(
        self, mock_request, mock_client, mock_company_response, mock_customization_response
    ):
        """Test full replacement of customization"""
        mock_request.side_effect = [
            mock_company_response,
            mock_customization_response,
            mock_customization_response
        ]
        
        company = mock_client.orgs.get(526)
        customization = company.customization
        
        # Replace with all fields
        new_data = {
            "suppress_pod": True,
            "list_land_default": 5,
            "has_sims_enabled": False,
            "has_devices_enabled": True,
            "has_device_uptime_report_enabled": True,
            "prominent_sim_field": "iccid",
            "prominent_device_field": "name",
            "has_event_notifications_enabled": False,
            "ignore_global_visible_items": True,
            "allow_sim_immunization": False,
            "allow_own_sim_provisioning": True,
            "allow_insecure_mqtt_reg": True,
            "default_device_pdr": 1800,
            "default_device_kai": 1000,
        }
        updated = customization.replace(**new_data)
        
        assert isinstance(updated, Customization)
        
        # Verify PUT was called
        args, kwargs = mock_request.call_args
        assert args[0] == "PUT"
        assert kwargs.get("json") == new_data
    
    def test_customization_without_client_raises_error(
        self, mock_client, mock_company_response
    ):
        """Test that accessing customization without client raises error"""
        with patch.object(ConnectClient, "_make_request") as mock_request:
            mock_request.return_value = mock_company_response
            
            company = mock_client.orgs.get(526)
            # Simulate no client
            company._client = None
            
            with pytest.raises(RuntimeError, match="Client not available"):
                _ = company.customization


class TestProfileModel:
    """Test suite for Profile model"""
    
    def test_profile_from_dict(self, mock_profile_response):
        """Test creating Profile from dictionary"""
        profile = Profile.from_dict(mock_profile_response)
        
        assert profile.company == 526
        assert profile.phone == "0123456789"
        assert profile.acct_code == "TRIN001"
        assert profile.month_start_day == 2
        assert profile.active_tenant_seeker is False
        assert profile.max_api_hits == 3000
        assert profile.external_ref is None
    
    def test_profile_attributes(self):
        """Test Profile attributes are accessible"""
        profile = Profile(
            company=526,
            url="http://test.com/profile/526/",
            phone="1234567890",
            acct_code="TEST001",
            month_start_day=1,
            mqtt_cid="12345678",
            description="Test",
            active_tenant_seeker=True,
            api_token="test-token",
            max_api_hits=1000,
            external_ref="ext-ref",
        )
        
        assert profile.company == 526
        assert profile.phone == "1234567890"
        assert profile.active_tenant_seeker is True


class TestCustomizationModel:
    """Test suite for Customization model"""
    
    def test_customization_from_dict(self, mock_customization_response):
        """Test creating Customization from dictionary"""
        customization = Customization.from_dict(mock_customization_response)
        
        assert customization.company == 526
        assert customization.has_sims_enabled is True
        assert customization.has_devices_enabled is True
        assert customization.prominent_sim_field == "msisdn"
        assert customization.prominent_device_field == "uid"
        assert customization.default_device_pdr == 1740
    
    def test_customization_attributes(self):
        """Test Customization attributes are accessible"""
        customization = Customization(
            url="http://test.com/customization/526/",
            company=526,
            company_url="http://test.com/company/526/",
            suppress_pod=True,
            list_land_default=5,
            has_sims_enabled=False,
            has_devices_enabled=True,
            has_device_uptime_report_enabled=True,
            prominent_sim_field="iccid",
            prominent_device_field="name",
            has_event_notifications_enabled=False,
            ignore_global_visible_items=True,
            allow_sim_immunization=False,
            allow_own_sim_provisioning=True,
            allow_insecure_mqtt_reg=True,
            default_device_pdr=1800,
            default_device_kai=1000,
        )
        
        assert customization.company == 526
        assert customization.has_sims_enabled is False
        assert customization.prominent_device_field == "name"
```

---

### Phase 5: Documentation (2-3 hours)

#### 5.1 Update README.md

Add section on Profile and Customization:

````markdown
## Company Profile and Customization

### Access Company Profile

```python
# Get company
company = client.orgs.get(company_id=526)

# Access profile
profile = company.profile
print(f"Phone: {profile.phone}")
print(f"Account Code: {profile.acct_code}")
print(f"API Token: {profile.api_token}")
```

### Update Profile

```python
# Update specific fields
updated_profile = profile.update(
    phone="0112345678",
    description="Updated company description"
)
```

### Access Customization Settings

```python
# Get customization
customization = company.customization
print(f"SIMs Enabled: {customization.has_sims_enabled}")
print(f"Devices Enabled: {customization.has_devices_enabled}")
print(f"Prominent Device Field: {customization.prominent_device_field}")
```

### Update Customization

```python
# Partial update (PATCH)
updated = customization.update(
    has_sims_enabled=False,
    prominent_device_field="name"
)

# Full replacement (PUT)
updated = customization.replace(
    suppress_pod=True,
    list_land_default=5,
    has_sims_enabled=True,
    has_devices_enabled=True,
    # ... all fields required
)
```
````

#### 5.2 Update docs/index.md

Add similar content with concise examples.

---

## Implementation Checklist

### Models
- [ ] Create `Profile` dataclass model
- [ ] Create `Customization` dataclass model
- [ ] Add `update()` method to Profile
- [ ] Add `update()` and `replace()` methods to Customization
- [ ] Update model exports in `__init__.py`

### Client
- [ ] Enhance `_make_request()` to support PATCH, PUT methods
- [ ] Handle 204 No Content responses
- [ ] Update error handling for different status codes

### Company Model
- [ ] Add `profile` property
- [ ] Add `customization` property
- [ ] Add proper error handling for missing client

### Tests
- [ ] Create mock fixtures for Profile and Customization
- [ ] Test Profile retrieval
- [ ] Test Profile update
- [ ] Test Customization retrieval
- [ ] Test Customization PATCH update
- [ ] Test Customization PUT replacement
- [ ] Test error cases (no client, API errors)
- [ ] Test model creation from dictionaries
- [ ] Test model attributes

### Documentation
- [ ] Update README.md with examples
- [ ] Update docs/index.md
- [ ] Add inline docstrings
- [ ] Add type hints

---

## File Structure

```
src/trinity_connect_client/
├── models/
│   ├── __init__.py (update exports)
│   └── org.py (add Profile and Customization classes)
├── main.py (enhance _make_request)
└── modules/
    └── orgs/
        └── __init__.py (no changes needed)

tests/
├── conftest.py (add mock fixtures)
└── modules/
    └── orgs/
        └── test_orgs_api.py (add test classes)
```

---

## Usage Examples

### Basic Usage

```python
from trinity_connect_client import ConnectClient

client = ConnectClient(
    base_url="https://capi.trintel.co.za",
    token="your-service-account-token"
)

# Get company
company = client.orgs.get(526)

# Access profile
profile = company.profile
print(f"Company: {company.name}")
print(f"Phone: {profile.phone}")
print(f"API Token: {profile.api_token}")

# Update profile
updated_profile = profile.update(
    phone="0112345678",
    description="Updated description"
)

# Access customization
customization = company.customization
print(f"SIMs Enabled: {customization.has_sims_enabled}")
print(f"Default Device Field: {customization.prominent_device_field}")

# Update customization
updated_customization = customization.update(
    has_sims_enabled=False,
    prominent_device_field="name"
)
```

### Error Handling

```python
from trinity_connect_client.exceptions import (
    ResourceNotFoundError,
    UnauthorisedError,
    ConnectAPIError
)

try:
    company = client.orgs.get(999)
    profile = company.profile
    profile.update(phone="invalid")
except ResourceNotFoundError:
    print("Company not found")
except UnauthorisedError:
    print("Access denied")
except ConnectAPIError as e:
    print(f"API error: {e}")
```

---

## Success Criteria

✅ Profile and Customization models created with all fields  
✅ Models support `from_dict()` classmethod  
✅ Profile has `update()` method (PATCH)  
✅ Customization has `update()` (PATCH) and `replace()` (PUT) methods  
✅ Company model has `profile` and `customization` properties  
✅ Client supports PATCH and PUT HTTP methods  
✅ Comprehensive test coverage (>90%)  
✅ All tests pass  
✅ Documentation updated with examples  
✅ Type hints on all models and methods  
✅ Error handling for missing client  
✅ Code follows existing patterns and style  

---

## Notes and Considerations

### Singleton Resources
Unlike folders (which are collections), Profile and Customization are **singleton resources** - there's only one per company. Therefore:
- No need for query builders (no `.all()`, `.filter()`, `.get()`)
- Properties return the model instance directly, not a builder
- No pagination support needed

### HTTP Methods
- **Profile**: Only PATCH for updates (no PUT)
- **Customization**: Both PATCH (partial) and PUT (full replacement)
- Neither supports POST (creation) or DELETE

### Field Validation
Consider adding validation for:
- `month_start_day`: Should be 1-28
- `phone`: Should be valid phone format
- Boolean fields: Ensure only True/False
- Integer fields: Ensure positive values

### Future Enhancements
- Add field validation
- Add convenience methods for common operations
- Add caching to avoid repeated API calls
- Add dirty tracking to only send changed fields

---

## Questions for User

Before implementation, please confirm:

1. **Field Validation**: Should we add validation for fields like `month_start_day` (1-28), phone format, etc.?

2. **Caching**: Should we cache the profile/customization instances to avoid repeated API calls?

3. **Dirty Tracking**: Should we track which fields changed and only send those in updates?

4. **Convenience Methods**: Should we add convenience methods like:
   - `profile.update_phone(new_phone)`
   - `customization.enable_sims()`
   - `customization.disable_sims()`

5. **Error Messages**: Should we provide more specific error messages for validation failures?

---

## Next Steps

1. **Review this plan** and provide feedback
2. **Confirm any questions** above
3. **Begin implementation** following the phases outlined
4. **Test thoroughly** with both unit and integration tests
5. **Update documentation** with actual usage examples

**Ready to implement!** 🚀
