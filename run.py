import asyncio

from chat_websockets import reconnect_to_websocket
from freeGPT import freeGPT
from utils.handle_providers_json import update_providers_json
from utils.config import Config

# if __name__ == "__main__":
#     fg = freeGPT()
#     update_providers_json(fg)
#     print("...........websocket_client starting.........", "info")

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(reconnect_to_websocket(fg))
#     loop.close()


# async def main():
#     config = Config().getConfig()
#     fg = freeGPT()
#     if not config["useDefault"]:
#         update_providers_json(fg)
#     print("...........websocket_client starting.........", "info")
#     await reconnect_to_websocket(fg)


if __name__ == "__main__":
    # asyncio.run(main())
    config = Config().getConfig()
    fg = freeGPT()
    if not config["useDefault"]:
        update_providers_json(fg)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(reconnect_to_websocket(fg))
    loop.close()
