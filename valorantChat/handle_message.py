import json
import time

from utils import read_init_prompt
from utils.discord_webhook import send_to_discord

from utils.logger import print_colored

config = json.load(open(r"config.json", encoding="utf8"))
id_seen = []
avoidList = config["players_to_avoid"]
avoidList.append(config["in_game_name"])
webhook_url = config["discord_webhook_url"]
prompt_path = config["prompt"]
update_frequency = config["providers-update-frequency"]

def handle(response, endpoint,fg):
    if len(response) > 10:
        resp_json = json.loads(response)
        message = resp_json[2]["data"]["messages"][0]
        if "ares-coregame" in message["cid"]:
            if message["id"] not in id_seen:
                sent_msg = f"{message['game_name']} : {message['body']}"
                if message["game_name"] not in avoidList:
                    time.sleep(3)
                    content = read_init_prompt(prompt_path)
                    content_prompt = content + sent_msg
                    res = fg.try_all_working_providers(content_prompt)
                    if len(res) > 200:
                        if webhook_url:
                            send_to_discord(
                                webhook_url,
                                f"```!!THIS MESSAGE WAS NOT SENT FOR BEING TOO LONG!! {sent_msg}\nchatGPT: {res}```",
                            )
                        print_colored(
                            f"!!THIS MESSAGE WAS NOT SENT FOR BEING TOO LONG!! - > chatGPT: {res}",
                            "error",
                        )
                    else:
                        try:
                            endpoint.postNewChatMessage(message["cid"], res)
                        except Exception as e:
                            print_colored(
                                "Failed To Send Message in Valorant ...", "error"
                            )
                        if webhook_url:
                            send_to_discord(
                                webhook_url, f"```{sent_msg}\nchatGPT: {res}```"
                            )
                        print_colored(f"chatGPT: {res}", "info")
                else:
                    if webhook_url:
                        send_to_discord(webhook_url, f"```{sent_msg}```")

                    print_colored(f"chatGPT: {res}", "info")

                id_seen.append(message["id"])