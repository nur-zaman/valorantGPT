
import ssl

import urllib3
import websockets.client

import websockets
from valorantChat.handle_message import handle
from valorantChat.ingameChat import Endpoints


async def reconnect_to_websocket(fg):
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
            h = handle(response, endpoint,fg)
            if h is not None:
                await websocket.close()
                return h