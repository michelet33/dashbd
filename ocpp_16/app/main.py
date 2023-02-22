import os
import logging
import asyncio
import uvicorn
# from enums import OcppMisc as oc
# from ocpp.routing import on
# from ocpp.v16 import ChargePoint as cp
# from ocpp.v16.enums import Action, RegistrationStatus, AuthorizationStatus, ResetType, ResetStatus
# from ocpp.v16 import call_result, call
from datetime import datetime
from fastapi import Body, FastAPI, status, Request, WebSocket, Depends
from models.Central_System import CentralSystem
from models.Charge_Point_16 import ChargePoint16

app = FastAPI()
now = datetime.now()
file = now.strftime("%Y%m%d")
filename= os.path.join(os.getcwd(), f'log/ws_ocpp_{file}.log')
logging.basicConfig(filename=filename,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

csms = CentralSystem()

# class ChargePoint(cp):
#
#     @on(Action.Heartbeat)  # this is an OCPP function, not important here
#     async def on_HB(self):
#         print("heart beat received from chargepoint")
#         return call_result.HeartbeatPayload(current_time=datetime.utcnow().isoformat()
#
#     async def reset(self, type: ResetType):
#         return await self.call(call.ResetPayload(type=type))


# class CentralSystem:
#     def __init__(self):
#         self._chargers = {}
#
#     def register_charger(self, cp: ChargePoint):
#         queue = asyncio.Queue(maxsize=1)
#         task = asyncio.create_task(self.start_charger(cp, queue))
#         self._chargers[cp] = task  # here I store the charger websocket incoming connection as cp task
#         print(self._chargers)
#         return queue
#
#     async def start_charger(self, cp, queue):
#         try:
#             await cp.start()
#         except Exception as error:
#             print(f"Charger {cp.id} disconnected: {error}")
#         finally:
#             del self._chargers[cp]
#             await queue.put(True)
#
#     async def reset_fun(self, cp_id: str, rst_type: str):
#         print(self._chargers.items())  # Now over here i see that _chargers is empty !!! why?
#         for cp, task in self._chargers.items():
#             print(cp.id)
#             if cp.id == cp_id:
#                 print("reached here")
#                 await cp.reset(rst_type)


class SocketAdapter:
    def __init__(self, websocket: WebSocket):
        self._ws = websocket

    async def recv(self) -> str:
        return await self._ws.receive_text()

    async def send(self, msg) -> str:
        await self._ws.send_text(msg)


@app.websocket("/ocpp/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, csms: CentralSystem = Depends(CentralSystem)):
    await websocket.accept(subprotocol='ocpp1.6')
    charge_point_id = websocket.url.path.strip('/')
    cp_id = charge_point_id[len(charge_point_id) - 1]
    cp = ChargePoint16(cp_id, SocketAdapter(websocket))
    logging.info(f"charger {cp.id} connected.")

    queue = csms.register_charger(
        cp)  # here i use the register_charger funtion to save the charge point class based websocket instance.
    await queue.get()

@app.websocket("/ws")
async def websocket_frontendpoint(websocket: WebSocket):
    await websocket.accept(subprotocol='ocpp1.6')
    while True:
        data = await websocket.receive_text()
        data = data.split(',')
        cps = csms.get_chargers()
        # cp = ChargePoint16()
        logging.info(cps)
        # find charger
        for e in enumerate(cps):
            cp = cps[e]
            logging.log(data[2])
            logging.log(cp.id)
            if cp.id == data[2]:
                logging.info('UPDATE FIRMWARE step1')
                await cp.send_update_firmware(data)
                break

@app.post("/reset")
async def reset(request: Request, cms: CentralSystem = Depends(CentralSystem)):
    data = await request.json()
    logging.info(f"API DATA to confirm {data}")
    get_response = await cms.reset_fun(data["cp_id"], data[
        "type"])  # here i call the reset_fun but as inside it there is no charger stored inside _chargers it gets no response.
    logging.info(f"==> The response from charger==> {get_response}")
    return "sucess"


if __name__ == '__main__':
    uvicorn.run(app, host='192.168.1.129', port=9001)