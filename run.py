import asyncio
import datetime
import json
import os
import ssl
import time

import requests
import urllib3
import websockets
import websockets.client

from endpoints import Endpoints
from freeGPT import freeGPT

config = json.load(open(r"config.json", encoding="utf8"))

id_seen = []

avoidList = config["players_to_avoid"]

avoidList.append(config["in_game_name"])

webhook_url = config["discord_webhook_url"]

prompt_path = config["prompt"]

update_frequency = config["providers-update-frequency"]


fg = freeGPT()


# Check if provider.json exists
if os.path.exists("providers.json"):
    with open("providers.json", "r") as json_file:
        existing_data = json.load(json_file)
    last_updated = existing_data.get("updated-on", "")

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    if last_updated != today:
        # The file was last updated on a different date, so update it
        print("Checking availabe free providers...")
        fg.update_working_providers()
        print("Done ")
        data = {
            "updated-on": today,
            "providers": [_provider.__name__ for _provider in fg.WORKING_PROVIDERS],
        }
        providers = fg.WORKING_PROVIDERS

        with open("providers.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        print("Data updated in providers.json")
    else:
        # The file was updated today, so read the providers array
        providers = existing_data.get("providers", [])
        fg.update_working_providers_from_name(providers)
        print("Providers :", providers)
else:
    # If provider.json doesn't exist, create it with today's date
    print("Checking availabe free providers...")
    fg.update_working_providers()
    print("Done ")
    data = {
        "updated-on": datetime.datetime.now().strftime("%Y-%m-%d"),
        "providers": [_provider.__name__ for _provider in fg.WORKING_PROVIDERS],
    }

    with open("providers.json", "w") as json_file:
        json.dump(data, json_file, indent=4)


async def recconect_to_websocket():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    endpoint = Endpoints()
    headers = endpoint.headers
    port = endpoint.port

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    url = f"wss://127.0.0.1:{port}"
    websocket_client = websockets.connect(url, ssl=ssl_context, extra_headers=headers)

    async with websocket_client as websocket:
        await websocket.send('[5, "OnJsonApiEvent_chat_v6_messages"]')
        while True:
            response = await websocket.recv()
            h = handle(response, endpoint)
            if h is not None:
                await websocket.close()
                return h


def readInitPrompt(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    return content


def send_to_discord(webhook_url, message):
    data = {"content": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    if response.status_code == 204:
        print("Webhook sent successfully")
    else:
        print("Failed to send webhook. Status code:", response.status_code)


def handle(response, endpoint):
    if len(response) > 10:
        resp_json = json.loads(response)
        message = resp_json[2]["data"]["messages"][0]
        # print(message)
        if "ares-coregame" in message["cid"]:
            if message["id"] not in id_seen:
                sentMsg = (
                    f"{message['game_name']}#{message['game_tag']} : {message['body']}"
                )
                sentMsg = f"{message['game_name']} : {message['body']}"
                # print("IN GAME NAME", message["game_name"])
                if message["game_name"] not in avoidList:
                    time.sleep(3)
                    content = readInitPrompt(prompt_path)
                    content_prompt = content + sentMsg
                    response = fg.try_all_working_providers(content_prompt)
                    if len(response) > 200:
                        if webhook_url != "":
                            send_to_discord(
                                webhook_url,
                                f"```!!THIS MESSAGE WAS NOT SENT FOR BEING TOO LONG!! {sentMsg}\nchatGPT: {response}```",
                            )
                        print(
                            f"!!THIS MESSAGE WAS NOT SENT FOR BEING TOO LONG!! - > chatGPT: {response}"
                        )
                    else:
                        try:
                            endpoint.postNewChatMessage(message["cid"], response)
                        except Exception as e:
                            print("Failed To Send Message in Valorant ...")
                        if webhook_url != "":
                            send_to_discord(
                                webhook_url, f"```{sentMsg}\nchatGPT: {response}```"
                            )
                        print(f"chatGPT: {response}")
                else:
                    if webhook_url != "":
                        send_to_discord(webhook_url, f"```{sentMsg}```")

                    print(f"chatGPT: {response}")

                id_seen.append(message["id"])


print("...........websocket_client starting.........")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(recconect_to_websocket())
loop.close()
