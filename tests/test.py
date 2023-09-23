import sys
import json
import datetime
import os

sys.path.insert(0, r"..\valorantGPT")
from freeGPT import freeGPT

config = json.load(open(r"config.json", encoding="utf8"))
system = """Pretend you are currently playing valorant and you are a very supportive teammate. Reply to the messages while staying in charater.

There are some ingame-language too that you should know,
gg = Good game
ggwp = good game well played
nc = nice
ff = surrender
mb = my bad
nt = nice try
you won't use these in your reply but you will understand what others mean when they write it.
No need to say things like "As a supportive teammate in Valorant, I would respond:"
just give me the reponse without quote
I'll attach the rule with every message but you will only reply with the response. Now let's test it out.
my input format will be . `<username> : <user's message>`

My Message:
"""


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


print("Started")
while True:
    prompt = input()
    prompt = system + prompt
    res = fg.try_all_working_providers(prompt)
    print(res)
