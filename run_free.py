import websockets
import websockets.client
import ssl
import json
import urllib3
import asyncio
from endpoints import Endpoints
import requests
import json
import time

import freeGPT


fg = freeGPT()
print("Checking availabe free providers...")
fg.update_working_providers()
print("Done ")
if len(fg.WORKING_PROVIDERS)==0:
    print("NO FREE PROVIDER AVAILABE !!")
config = json.load(open(r"config.json", encoding="utf8"))

id_seen = []

avoidList = config["players_to_avoid"]

avoidList.append(config["in_game_name"])

webhook_url = config["discord_webhook_url"]


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
                if message["game_name"] not in avoidList:
                    time.sleep(10)
                    content = readInitPrompt(r"prompt.txt")
                    content_prompt = content + sentMsg
                    response = fg.try_all_working_providers(content_prompt)

                    endpoint.postNewChatMessage(message["cid"], response)

                    if webhook_url != "":
                        send_to_discord(
                            webhook_url, f"```{sentMsg}\nchatGPT: {response}```"
                        )

                    print(sentMsg)
                    print(f"chatGPT: {response}")
                else:
                    if webhook_url != "":
                        send_to_discord(webhook_url, f"```{sentMsg}```")

                    print(sentMsg)

                id_seen.append(message["id"])


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(recconect_to_websocket())
loop.close()
