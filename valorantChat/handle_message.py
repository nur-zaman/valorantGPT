import json
import time
import sys
from pathlib import Path

from utils import read_init_prompt
from utils.discord_webhook import send_to_discord

from utils.logger import print_colored
from utils.config import Config

sys.path.append(str(Path(__file__).parent.parent))
from freeGPT import freeGPT
from freeGPT.defaults import useChatCompletion

config = Config().getConfig()

id_seen = []
avoidList = config["players_to_avoid"]
# avoidList.append(Config["in_game_name"])
webhook_url = config["discord_webhook_url"]
prompt_path = config["prompt"]
useDefault = config["useDefault"]


async def handle(response, endpoint, fg: freeGPT):
    if len(response) > 10:
        resp_json = json.loads(response)
        message = resp_json[2]["data"]["messages"][0]
        print(message)
        if ("ares-coregame" in message["cid"]) or ("ares-parties" in message["cid"]):
            if message["id"] not in id_seen:
                sent_msg = f"{message['game_name']} : {message['body']}"
                if message["game_name"] not in avoidList:
                    content = read_init_prompt(prompt_path)
                    content_prompt = content + sent_msg
                    print("sending - >", sent_msg)

                    res = ""
                    if useDefault:
                        res = useChatCompletion(prompt=content_prompt)
                    else:
                        res = await fg.try_random_provider(content_prompt)

                    if len(res) > 200:
                        if webhook_url:
                            send_to_discord(
                                webhook_url,
                                f"```!!THIS MESSAGE WAS NOT SENT FOR BEING TOO LONG!! {sent_msg}\nchatGPT: {res}```",
                            )
                        print_colored(
                            f"{sent_msg}\n!!THIS MESSAGE WAS NOT SENT FOR BEING TOO LONG!! - > chatGPT: {res}",
                            "error",
                        )
                    else:
                        try:
                            endpoint.postNewChatMessage(message["cid"], res)
                        except Exception as e:
                            print_colored(
                                "{res}Failed To Send Message in Valorant ...", "error"
                            )
                        if webhook_url:
                            send_to_discord(
                                webhook_url, f"```{sent_msg}\nchatGPT: {res}```"
                            )
                            print_colored(f"{sent_msg}\nchatGPT: {res}", "info")
                else:
                    if webhook_url:
                        send_to_discord(
                            webhook_url,
                            f"```{sent_msg}\n( Ignored because of avoid list)```",
                        )

                    print_colored(f"Ignored because of avoid list : \n{avoidList}")

                id_seen.append(message["id"])
