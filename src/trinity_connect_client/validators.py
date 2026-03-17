def validate_id(i):
    if not isinstance(i, int) or i <= 0:
        raise ValueError("ID must be a positive integer")


def validate_uid(u):
    if not isinstance(u, str) or not u.strip():
        raise ValueError("UID must be a non-empty string")


def validate_command(command):
    if not isinstance(command, dict):
        raise ValueError("Command must be a dictionary")

    required_fields = {"rpc", "args", "pid", "ttl", "qos"}
    if not required_fields.issubset(command.keys()):
        missing = required_fields - command.keys()
        raise ValueError(f"Command missing required fields: {missing}")

    if not isinstance(command["rpc"], str):
        raise ValueError("Command 'rpc' must be a string")

    if not isinstance(command["args"], list):
        raise ValueError("Command 'args' must be a list")

    if not isinstance(command["pid"], (str, int)):
        raise ValueError("Command 'pid' must be a string or integer")

    if not isinstance(command["ttl"], (int, float)) or command["ttl"] < 0:
        raise ValueError("Command 'ttl' must be a non-negative number")

    if not isinstance(command["qos"], int) or command["qos"] < 0:
        raise ValueError("Command 'qos' must be a non-negative integer")


def validate_device_create_request(data):
    if not isinstance(data, dict):
        raise ValueError("Device data must be a dictionary")

    ALLOWED_FIELDS = {
        "folder",
        "uid",
        "name",
        "description",
        "state",
        "tpp_id",
        "imei",
        "imei2",
        "serial_number",
        "comm_interval_contract",
        "command_model",
        "data_lens",
        "event_lens",
        "profile",
        "category_id",
    }

    cleaned_data = {k: v for k, v in data.items() if k in ALLOWED_FIELDS}

    if "folder" not in cleaned_data:
        raise ValueError("Device creation requires 'folder' field")

    if "uid" not in cleaned_data:
        raise ValueError("Device creation requires 'uid' field")

    validate_id(cleaned_data["folder"])

    uid = cleaned_data["uid"]
    if not isinstance(uid, str):
        raise ValueError("Device 'uid' must be a string")
    if not uid.strip():
        raise ValueError("Device 'uid' must be a non-empty string")
    if not uid.isalnum():
        raise ValueError(
            "Device 'uid' must contain only alphanumeric characters (0-9, A-Z)"
        )
    if not uid.isupper() and not uid.isdigit():
        raise ValueError("Device 'uid' must contain only uppercase letters and digits")
    if not (15 <= len(uid) <= 20):
        raise ValueError("Device 'uid' must be between 15 and 20 characters long")

    if "state" in cleaned_data:
        valid_states = [50, 51, 52, 53, 27, 33, 20, 1]
        if cleaned_data["state"] not in valid_states:
            raise ValueError(
                f"Invalid device state: {cleaned_data['state']}. Must be one of {valid_states}"
            )

    if "imei" in cleaned_data and cleaned_data.get("imei"):
        if len(str(cleaned_data["imei"])) > 15:
            raise ValueError("Device 'imei' must not exceed 15 characters")

    if "imei2" in cleaned_data and cleaned_data.get("imei2"):
        if len(str(cleaned_data["imei2"])) > 15:
            raise ValueError("Device 'imei2' must not exceed 15 characters")

    if "serial_number" in cleaned_data and cleaned_data.get("serial_number"):
        if len(str(cleaned_data["serial_number"])) > 30:
            raise ValueError("Device 'serial_number' must not exceed 30 characters")

    if "tpp_id" in cleaned_data and cleaned_data.get("tpp_id"):
        if len(str(cleaned_data["tpp_id"])) > 32:
            raise ValueError("Device 'tpp_id' must not exceed 32 characters")

    if "category_id" in cleaned_data and cleaned_data.get("category_id") is not None:
        if not isinstance(cleaned_data["category_id"], int):
            raise ValueError("Device 'category_id' must be an integer")
        if cleaned_data["category_id"] <= 0:
            raise ValueError("Device 'category_id' must be a positive integer")

    return cleaned_data
