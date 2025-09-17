PATH_MAP = {
    "v4": {
        "device_by_id": "devices/{device_id}/",
        "device_by_uid": "devices/uid/{device_uid}/",
        "device_latest_data": "devices/uid/{device_uid}/data/latest/",
        "device_events_by_uid": "devices/uid/{device_uid}/events/",
        "device_commands_by_uid": "devices/uid/{device_uid}/commands/",
        "list_by_folder": "devices/folder/{folder_id}/",
        "list_by_folder_lite": "devices/folder/{folder_id}/lite/",
        "issue_command": "devices/{device_id}/command/send/",
        "issue_command_by_uid": "devices/uid/{device_uid}/command/send/",
    }
}
