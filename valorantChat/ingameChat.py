import requests
import urllib3
from exceptions import ValorantAPIError
from valorantChat.auth import Auth


class Endpoints:
    def __init__(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        auth = Auth()
        self.headers = auth.getHeaders()
        self.config = auth.getConfig()
        self.port = self.config["port"]

    def gameGetRequest(self, endpoint):
        response = requests.get(
            "https://127.0.0.1:{port}{endpoint}".format(
                port=self.port, endpoint=endpoint
            ),
            headers=self.headers,
            verify=False,
        )

        # custom exceptions for http status codes
        self.__verify_status_code(response.status_code)

        try:
            r = response.json()
            return r
        except:
            raise ValorantAPIError("An error ocurred trying to get game APIs")

    def __gamePostRequest(self, endpoint, data):
        response = requests.post(
            "https://127.0.0.1:{port}{endpoint}".format(
                port=self.port, endpoint=endpoint
            ),
            headers=self.headers,
            verify=False,
            json=data,
        )

        # custom exceptions for http status codes
        self.__verify_status_code(response.status_code)

        try:
            r = response.json()
            return r
        except:
            raise ValorantAPIError("An error ocurred trying to get game APIs")

    def __verify_status_code(self, status_code):
        """Verify that the request was successful according to exceptions"""
        if status_code in [404, 401, 500]:
            raise ValorantAPIError("An invalid status code returned from game APIs")

    def getChatToken(self):
        return self.gameGetRequest("/chat/v6/conversations/ares-coregame")

    def getChatHistorty(self, cid):
        return self.gameGetRequest(f"/chat/v6/messages?cid={cid}")

    def postNewChatMessage(self, cid, message):
        data = {"cid": cid, "message": message, "type": "groupchat"}
        return self.__gamePostRequest("/chat/v6/messages", data)
