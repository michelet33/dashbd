# coding: utf-8
import json
import os
import logging
import uvicorn
from datetime import datetime
from fastapi import FastAPI, WebSocket, Depends
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

class SocketAdapter:
    def __init__(self, websocket: WebSocket):
        self._ws = websocket

    async def recv(self) -> str:
        return await self._ws.receive_text()

    async def send(self, msg) -> str:
        await self._ws.send_text(msg)


@app.websocket("/ocpp/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
# async def websocket_endpoint(websocket: WebSocket, client_id: str, csms: CentralSystem = Depends(CentralSystem)):
    await websocket.accept(subprotocol='ocpp1.6')
    charge_point_id = websocket.url.path.split('/')
    # logging.info(charge_point_id)
    cp_id = charge_point_id[len(charge_point_id) - 1]
    chargers = csms.get_chargers()
    if cp_id not in chargers.keys():
        cp = ChargePoint16(cp_id, SocketAdapter(websocket))
        logging.info(f"charger {cp.id} connected : {client_id}")
        # use the register_charger funtion to save the charge point class based websocket instance.
        queue = csms.register_charger(cp)
        await queue.get()

@app.websocket("/ws")
async def websocket_frontendpoint(websocket: WebSocket):
    await websocket.accept(subprotocol='ocpp1.6')
    while True:
        data = await websocket.receive_text()
        logging.info(data)
        data = json.loads(data)
        logging.info(data)
        chargers = csms.get_chargers()

        logging.info(csms)
        logging.info(chargers.items)
        for cp, task in chargers.items():
            logging.info(data["charger"])
            logging.info(cp.id)
            if cp.id == data["charger"]:
                logging.info('UPDATE FIRMWARE step1')
                await cp.send_update_firmware(data['content'])
                await websocket.send_text(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {data['action']}: "
                                          f"{data['content']}")
                break

# @app.post("/reset")
# async def reset(request: Request, cms: CentralSystem = Depends(CentralSystem)):
#     data = await request.json()
#     logging.info(f"API DATA to confirm {data}")
#     get_response = await cms.reset_fun(data["cp_id"], data[
#         "type"])  # here I call the reset_fun but as inside it there is no charger stored inside _chargers it gets no response.
#     logging.info(f"==> The response from charger==> {get_response}")
#     return "sucess"


if __name__ == '__main__':
    uvicorn.run(app, host='192.168.1.129', port=9001)
