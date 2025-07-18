from typing import Dict

PATH_MAP: Dict[str, Dict[str, str]] = {
    "v4": {
        "company_by_id": "orgs/company/{company_id}/",
        "states": "orgs/company/states/",
        "company_folders": "orgs/folders/company/{company_id}/",
        "folder_by_id": "orgs/folder/{folder_id}/",
    }
}
