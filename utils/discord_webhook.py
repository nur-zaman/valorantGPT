import json

import requests

from utils.logger import print_colored


def send_to_discord(webhook_url, message):
    data = {"content": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    if response.status_code == 204:
        print_colored("Webhook sent successfully", "success")
    else:
        print_colored(
            f"Failed to send webhook. Status code: {response.status_code}", "error"
        )