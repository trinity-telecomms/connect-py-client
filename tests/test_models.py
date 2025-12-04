"""Tests for response models."""

from connect_client.models import Company, Device, DeviceCommand, DeviceData, DeviceEvent, Folder


class TestDevice:
    """Test suite for Device model"""

    def test_from_dict(self):
        """Test Device creation from dictionary"""
        data = {
            "id": 1,
            "url": "https://api.example.com/api/v4/devices/1/",
            "name": "Test Device",
            "description": "Mock device for testing",
            "state": 52,
            "t_type": 1,
            "tpp_id": None,
            "company": 1,
            "folder": 1,
            "state_display": "Activated",
            "t_type_display": "Device",
            "company_name": "Mock Company",
            "folder_name": "Mock Folder",
            "company_url": "https://api.example.com/api/v4/orgs/company/1/",
            "folder_url": "https://api.example.com/api/v4/orgs/folder/1/",
            "aux_values_url": "https://api.example.com/api/v4/adaptations/aux_values/thing/1/",
            "uid": "test-uid-123",
            "imei": "123456789012345",
            "imei2": "123456789012346",
            "serial_number": "SN-TEST-001",
            "comm_interval_contract": 10,
            "comm_state": 1,
            "comm_state_display": "Active",
            "youngest_comm_timestamp": "2024-01-01T00:00:00Z",
            "command_model": 1,
            "data_lens": 10,
            "event_lens": None,
            "profile": None,
            "commands_url": "https://api.example.com/api/v4/devices/1/commands/",
            "latest_data_url": "https://api.example.com/api/v4/devices/1/data/latest/",
            "events_url": "https://api.example.com/api/v4/devices/1/events/",
            "meta_url": "https://api.example.com/api/v4/devices/1/meta/",
            "geo_url": "https://api.example.com/api/v4/devices/1/geo/",
            "category_url": "https://api.example.com/api/v4/adaptations/category/device/1/",
            "tags_url": "https://api.example.com/api/v4/tags/thing/1/",
        }

        device = Device.from_dict(data)

        assert device.id == 1
        assert device.url == "https://api.example.com/api/v4/devices/1/"
        assert device.name == "Test Device"
        assert device.uid == "test-uid-123"
        assert device.state == 52
        assert device.state_display == "Activated"
        assert device.company == 1
        assert device.folder == 1
        assert device.tpp_id is None
        assert device.event_lens is None
        assert device.profile is None

    def test_device_attributes(self):
        """Test Device attributes are accessible"""
        device = Device(
            id=2,
            url="https://api.example.com/api/v4/devices/2/",
            name="Mock Device 2",
            description="Mock description",
            state=52,
            t_type=1,
            tpp_id=None,
            company=2,
            folder=2,
            state_display="Activated",
            t_type_display="Device",
            company_name="Mock Company 2",
            folder_name="Mock Folder 2",
            company_url="https://api.example.com/api/v4/orgs/company/2/",
            folder_url="https://api.example.com/api/v4/orgs/folder/2/",
            aux_values_url="https://api.example.com/api/v4/adaptations/aux_values/thing/2/",
            uid="test-uid-456",
            imei="223456789012345",
            imei2="223456789012346",
            serial_number="SN-TEST-002",
            comm_interval_contract=20,
            comm_state=2,
            comm_state_display="Inactive",
            youngest_comm_timestamp="2024-01-02T00:00:00Z",
            command_model=1,
            data_lens=20,
            event_lens=5,
            profile=1,
            commands_url="https://api.example.com/api/v4/devices/2/commands/",
            latest_data_url="https://api.example.com/api/v4/devices/2/data/latest/",
            events_url="https://api.example.com/api/v4/devices/2/events/",
            meta_url="https://api.example.com/api/v4/devices/2/meta/",
            geo_url="https://api.example.com/api/v4/devices/2/geo/",
            category_url="https://api.example.com/api/v4/adaptations/category/device/2/",
            tags_url="https://api.example.com/api/v4/tags/thing/2/",
        )

        assert device.id == 2
        assert device.uid == "test-uid-456"
        assert device.name == "Mock Device 2"
        assert device.state == 52
        assert device.company == 2
        assert device.folder == 2


class TestCompany:
    """Test suite for Company model"""

    def test_from_dict(self):
        """Test Company creation from dictionary"""
        data = {
            "id": 1,
            "url": "https://api.example.com/api/v4/orgs/company/1/",
            "name": "Test Company",
            "state": 52,
            "state_display": "Activated",
            "is_ee": False,
            "url_profile": "https://api.example.com/api/v4/orgs/profile/1/",
            "folder_url": "https://api.example.com/api/v4/orgs/folders/company/1/",
            "url_folder_tree": "https://api.example.com/api/v4/orgs/folders/company/1/tree/",
            "url_sims": "https://api.example.com/api/v4/sims/company/1/",
            "apn_urls": "https://api.example.com/api/v4/apns/company/1/",
            "url_devices": "https://api.example.com/api/v3/devices/company/1/list/",
            "url_budgets": "https://api.example.com/api/v4/budgets/data_budgets/company/1/",
            "url_access": "https://api.example.com/api/v4/members/access/company/1/",
            "url_tags": "https://api.example.com/api/v4/tags/company/1/",
            "url_contracts": "https://api.example.com/api/v4/contracts/company/1/",
            "url_adaptations": "https://api.example.com/api/v4/adaptations/company/1/",
        }

        company = Company.from_dict(data)

        assert company.id == 1
        assert company.url == "https://api.example.com/api/v4/orgs/company/1/"
        assert company.name == "Test Company"
        assert company.state == 52
        assert company.state_display == "Activated"
        assert company.is_ee is False

    def test_company_attributes(self):
        """Test Company attributes are accessible"""
        company = Company(
            id=2,
            url="https://api.example.com/api/v4/orgs/company/2/",
            name="Mock Company 2",
            state=52,
            state_display="Activated",
            is_ee=True,
            url_profile="https://api.example.com/api/v4/orgs/profile/2/",
            folder_url="https://api.example.com/api/v4/orgs/folders/company/2/",
            url_folder_tree="https://api.example.com/api/v4/orgs/folders/company/2/tree/",
            url_sims="https://api.example.com/api/v4/sims/company/2/",
            apn_urls="https://api.example.com/api/v4/apns/company/2/",
            url_devices="https://api.example.com/api/v3/devices/company/2/list/",
            url_budgets="https://api.example.com/api/v4/budgets/data_budgets/company/2/",
            url_access="https://api.example.com/api/v4/members/access/company/2/",
            url_tags="https://api.example.com/api/v4/tags/company/2/",
            url_contracts="https://api.example.com/api/v4/contracts/company/2/",
            url_adaptations="https://api.example.com/api/v4/adaptations/company/2/",
        )

        assert company.id == 2
        assert company.name == "Mock Company 2"
        assert company.state == 52
        assert company.is_ee is True


class TestFolder:
    """Test suite for Folder model"""

    def test_from_dict(self):
        """Test Folder creation from dictionary"""
        data = {
            "id": 1,
            "url": "/api/v4/orgs/folder/1/",
            "name": "Test Folder",
            "path": "/1",
            "human_path": "Test Company/Test Folder",
            "parent": 1,
            "url_sims": "https://api.example.com/api/v4/sims/folder/1/",
            "url_devices": "https://api.example.com/api/v4/devices/folder/1/",
            "tree_id": 1,
        }

        folder = Folder.from_dict(data)

        assert folder.id == 1
        assert folder.url == "/api/v4/orgs/folder/1/"
        assert folder.name == "Test Folder"
        assert folder.path == "/1"
        assert folder.human_path == "Test Company/Test Folder"
        assert folder.parent == 1
        assert folder.tree_id == 1

    def test_folder_attributes(self):
        """Test Folder attributes are accessible"""
        folder = Folder(
            id=2,
            url="/api/v4/orgs/folder/2/",
            name="Mock Folder 2",
            path="/2",
            human_path="Mock Company/Mock Folder 2",
            parent=2,
            url_sims="https://api.example.com/api/v4/sims/folder/2/",
            url_devices="https://api.example.com/api/v4/devices/folder/2/",
            tree_id=2,
        )

        assert folder.id == 2
        assert folder.name == "Mock Folder 2"
        assert folder.parent == 2
        assert folder.human_path == "Mock Company/Mock Folder 2"


class TestDeviceData:
    """Test suite for DeviceData model"""

    def test_from_dict(self):
        """Test DeviceData creation from dictionary"""
        data = {"temperature": 25.5, "humidity": 60}

        device_data = DeviceData.from_dict(data)

        assert device_data.data == data
        assert device_data.data["temperature"] == 25.5
        assert device_data.data["humidity"] == 60


class TestDeviceEvent:
    """Test suite for DeviceEvent model"""

    def test_from_dict_with_list(self):
        """Test DeviceEvent creation from list"""
        data = [
            {"event": "connected", "timestamp": "2023-01-01T00:00:00Z"},
            {"event": "disconnected", "timestamp": "2023-01-01T01:00:00Z"},
        ]

        device_event = DeviceEvent.from_dict(data)

        assert len(device_event.events) == 2
        assert device_event.events[0]["event"] == "connected"
        assert device_event.events[1]["event"] == "disconnected"

    def test_from_dict_with_events_key(self):
        """Test DeviceEvent creation from dict with events key"""
        data = {
            "events": [
                {"event": "alert", "timestamp": "2023-01-01T00:00:00Z"},
            ]
        }

        device_event = DeviceEvent.from_dict(data)

        assert len(device_event.events) == 1
        assert device_event.events[0]["event"] == "alert"


class TestDeviceCommand:
    """Test suite for DeviceCommand model"""

    def test_from_dict_with_list(self):
        """Test DeviceCommand creation from list"""
        data = [
            {"command": "reboot", "timestamp": "2023-01-01T00:00:00Z"},
            {"command": "update", "timestamp": "2023-01-01T01:00:00Z"},
        ]

        device_command = DeviceCommand.from_dict(data)

        assert len(device_command.commands) == 2
        assert device_command.commands[0]["command"] == "reboot"
        assert device_command.commands[1]["command"] == "update"

    def test_from_dict_with_commands_key(self):
        """Test DeviceCommand creation from dict with commands key"""
        data = {
            "commands": [
                {"command": "reset", "timestamp": "2023-01-01T00:00:00Z"},
            ]
        }

        device_command = DeviceCommand.from_dict(data)

        assert len(device_command.commands) == 1
        assert device_command.commands[0]["command"] == "reset"
