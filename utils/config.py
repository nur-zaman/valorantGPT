import json


class Config:
    config = json.load(open(r"config.json", encoding="utf8"))

    # avoidList = config["players_to_avoid"]
    # # avoidList.append(config["in_game_name"])
    # webhook_url = config["discord_webhook_url"]
    # prompt_path = config["prompt"]
    # update_frequency = config["providers-update-frequency"]
    def getDiscordWebhook(self):
        return self.config["discord_webhook_url"]

    def getConfig(self):
        return self.config


# id_seen = []
# # avoidList = list(Config["players_to_avoid"])
# # avoidList.append(Config["in_game_name"])
# print(config)
# print(config["discord_webhook_url"])
# print(config["prompt"])
# print(config["useDefault"])
