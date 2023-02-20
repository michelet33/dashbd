# coding: utf-8
import os
from functools import partial

# import uvicorn
# from fastapi import FastAPI
import asyncio
import websockets
import logging
from aiohttp import web
from dotenv import load_dotenv
# import models.Central_System as CS
from models.Central_System import CentralSystem
from models.Charge_Point_16 import ChargePoint16
# from api.request import ws

# app = FastAPI()
# app.include_router(ws)

load_dotenv('.env')
filename= os.path.join(os.getcwd(), 'ws_ocpp.log')
logging.basicConfig(filename=filename,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

async def on_connect(websocket, path, csms: CentralSystem):
    """ For every new charge point that connects, create a ChargePoint instance
    and start listening for messages.

    The ChargePoint is registered at the CSMS.

    """
    try:
        requested_protocols = websocket.request_headers["Sec-WebSocket-Protocol"]
    except KeyError:
        logging.error("Client hasn't requested any Subprotocol. Closing Connection")
        return await websocket.close()
    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        # In the websockets lib if no subprotocols are supported by the
        # client and the server, it proceeds without a subprotocol,
        # so we have to manually close the connection.
        logging.warning(
            "Protocols Mismatched | Expected Subprotocols: %s,"
            " but client supports  %s | Closing connection",
            websocket.available_subprotocols,
            requested_protocols,
        )
        return await websocket.close()
    charge_point_id = path.strip("/").split('/')
    charge_point_id= charge_point_id[len(charge_point_id)-1]
    cp = ChargePoint16(charge_point_id, websocket)
    print(f"Charger {cp.id} connected.")
    logging.info(f"Charger {cp.id} connected.")
    # If this handler returns the connection will be destroyed. Therefore we need some
    # synchronization mechanism that blocks until CSMS wants to close the connection.
    # An `asyncio.Queue` is used for that.
    queue = csms.register_charger(cp)
    await queue.get()


async def change_config(request):
    """ HTTP handler for changing configuration of all charge points. """
    data = await request.json()
    csms = request.app["csms"]

    await csms.change_configuration(data["key"], data["value"])

    return web.Response()


async def disconnect_charger(request):
    """ HTTP handler for disconnecting a charger. """
    data = await request.json()
    csms = request.app["csms"]

    try:
        csms.disconnect_charger(data["id"])
    except ValueError as e:
        print(f"Failed to disconnect charger: {e}")
        return web.Response(status=404)

    return web.Response()

async def create_websocket_server(csms: CentralSystem):
    handler = partial(on_connect, csms=csms)
    server = os.getenv('BACKEND_HOST')
    port = os.getenv('BACKEND_PORT')
    version= os.getenv('PROTOCOLE')
    return await websockets.serve(handler, server, port, subprotocols=[version])

#
# async def create_http_server(csms: CentralSystem):
#
#     server = os.getenv('BACKEND_HOST')
#     port = os.getenv('BACKEND_PORT')
#     application = web.Application()
#     application.add_routes([web.post("/ws", websocket_endpoint)])
#     application.add_routes([web.post("/disconnect", disconnect_charger)])
#     application.add_routes([web.post("/ocpp", change_config)])
#
#     # Put CSMS in app so it can be accessed from request handlers.
#     application["csms"] = csms
#
#     runner = web.AppRunner(application)
#     await runner.setup()
#
#     site = web.TCPSite(runner, server, port)
#     return site

async def main():
    server = os.getenv('HTTP_SERVER')
    port = int(os.getenv('SERVER_PORT'))
    csms = CentralSystem()
    websocket_server = await create_websocket_server(csms)
    # http_server = await create_http_server(csms)
    # await asyncio.wait([websocket_server.wait_closed(), http_server.start()])
    # await asyncio.wait([websocket_server.wait_closed(), uvicorn.run(app, host=server, port=port)])
    await websocket_server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
