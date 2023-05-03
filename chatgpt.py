from revChatGPT.V1 import Chatbot
import json


class ChatGPT:
    def __init__(self) -> None:
        self.config = json.load(open(r"config.json"))

        self.chatbot = Chatbot(self.config["chatgptToken"], conversation_id=None)
        self.content = ""

    def readInitPrompt(self, file_path):
        with open(file_path, "r") as f:
            content = f.read()
        return content

    def generate_response(self, prompt):
        response = ""
        for data in self.chatbot.ask(prompt):
            response = data["message"]
        return response
