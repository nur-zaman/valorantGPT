import sys
import json
import datetime
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import freeGPT

config = json.load(open(r"config.json", encoding="utf8"))

prompt_path = config["prompt"]
with open(prompt_path, "r") as f:
    system = f.read()


fg = freeGPT.freeGPT()


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


# start()

import freeGPT.defaults


def defaults():
    print("Started")
    while True:
        prompt = input()
        prompt = system + "\nnewr : " + prompt
        res = freeGPT.defaults.useChatCompletion(prompt=prompt)
        if len(res) > 0:
            print("print")
        print(len(res))
        print(res)


defaults()
