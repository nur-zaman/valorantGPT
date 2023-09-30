import sys
import json
import datetime
import os

sys.path.insert(0, r"..\valorantGPT")
from freeGPT import freeGPT

config = json.load(open(r"config.json", encoding="utf8"))

prompt_path = config["prompt"]
with open(prompt_path, "r") as f:
    system = f.read()


fg = freeGPT()


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


def start():
    print("Started")
    while True:
        prompt = input()
        prompt = system + "\nnewr : " + prompt
        res = fg.try_all_working_providers(prompt=prompt)
        if len(res) > 0:
            print("print")
        print(len(res))
        print(res)


start()
