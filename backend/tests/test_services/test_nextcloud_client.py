import os
import json
from caldav import DAVClient

def get_nextcloud_client():
    secrets_path = os.path.expanduser("~/.app_secrets/env.json")
    with open(secrets_path, "r") as f:
        secrets = json.load(f)
    url = secrets["NEXTCLOUD_URL"]
    username = secrets["NEXTCLOUD_USERNAME"]
    password = secrets["NEXTCLOUD_PASSWORD"]
    return DAVClient(url, username=username, password=password)
