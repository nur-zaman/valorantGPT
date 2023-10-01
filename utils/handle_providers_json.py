import os
from utils.logger import print_colored
import datetime
import json


def update_providers_json(fg):
    if os.path.exists("providers.json"):
        with open("providers.json", "r") as json_file:
            existing_data = json.load(json_file)
        last_updated = existing_data.get("updated-on", "")

        today = datetime.datetime.now().strftime("%Y-%m-%d")

        if last_updated != today:
            # The file was last updated on a different date, so update it
            print_colored("Checking available free providers...", "info")
            fg.update_working_providers()
            print_colored("Done", "success")
            data = {
                "updated-on": today,
                "providers": [_provider.__name__ for _provider in fg.WORKING_PROVIDERS],
            }
            providers = fg.WORKING_PROVIDERS

            with open("providers.json", "w") as json_file:
                json.dump(data, json_file, indent=4)

            print_colored("Data updated in providers.json", "success")
        else:
            # The file was updated today, so read the providers array
            providers = existing_data.get("providers", [])
            fg.update_working_providers_from_name(providers)
            print_colored("Providers: " + str(providers), "info")
    else:
        # If provider.json doesn't exist, create it with today's date
        print_colored("Checking available free providers...", "info")
        fg.update_working_providers()
        print_colored("Done", "success")
        data = {
            "updated-on": datetime.datetime.now().strftime("%Y-%m-%d"),
            "providers": [_provider.__name__ for _provider in fg.WORKING_PROVIDERS],
        }

        with open("providers.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
