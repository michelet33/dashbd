# coding: utf-8
import json
import os
import logging
import uvicorn
from datetime import datetime
import websockets.connection
from fastapi import FastAPI, WebSocket, Depends
from models.Central_System import CentralSystem
from models.Charge_Point_16 import ChargePoint16
from ocpp.v16 import call
from ocpp.v16.enums import MessageTrigger
import requests

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
    cp_id = charge_point_id[len(charge_point_id) - 1]
    chargers = csms.get_chargers()
    if cp_id not in chargers.keys():
        cp = ChargePoint16(cp_id, SocketAdapter(websocket))
        logging.info(f"charger {cp.id} connected : {client_id}")
        # use the register_charger funtion to save the charge point class based websocket instance.
        queue = await csms.register_charger(cp)
        # save
        status = [MessageTrigger.status_notification,
                  MessageTrigger.firmware_status_notification,
                  MessageTrigger.diagnostics_status_notification,
                  MessageTrigger.firmware_status_notification,
                  MessageTrigger.boot_notification,
                  MessageTrigger.meter_values]
        for s in status:
            request = call.TriggerMessagePayload(
                requested_message=s
            )
            await cp.call(request)
        await queue.get()

@app.websocket("/ws")
async def websocket_frontendpoint(websocket: WebSocket):
    # await websocket.accept()
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
                logging.info(data['content'])
                await cp.send_update_firmware(data['content'])
                await websocket.send_text(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {data['action']}: "
                                          f"{data['content']}")
                break

@app.websocket("/ws2")
async def websocket_robotfw(websocket: WebSocket):
    await websocket.accept()
    # await websocket.accept(subprotocol='ocpp1.6')
    while True:
        data = await websocket.receive_text()
        data = json.loads(data)
        logging.info(data)
        chargers = csms.get_chargers()
        logging.info(csms)
        logging.info(chargers.items)
        for cp, task in chargers.items():
            logging.info(data['charger'])
            logging.info(cp.id)
            if cp.id == data['charger']:
                logging.info('UPDATE FIRMWARE step1')
                logging.info(data['content'])
                await cp.send_update_firmware(data['content'])
                await websocket.send_text("Accepted")
                break
    await websockets.connection.CLOSED

@app.on_event("startup")
async def startup_event():
    # print('startup')
    LOGIN_ENDPOINT = "http://192.168.1.129:5000/"
    # LOGIN_ENDPOINT = "http://127.0.0.1:5000/"
    url = os.path.join(LOGIN_ENDPOINT, 'chargers/invalid/')
    requests.packages.urllib3.disable_warnings()
    response = requests.post(
        url=url,
        timeout=30,
        verify=False
    )
    response.raise_for_status()
    # print(response.content)



if __name__ == '__main__':
    uvicorn.run(app, host='192.168.1.129', port=9001)
