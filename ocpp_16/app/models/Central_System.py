# coding: utf-8
import inspect
import os
from datetime import datetime
from ocpp.v16 import ChargePoint
import asyncio
import logging
from . import utils

now = datetime.now()
file = now.strftime("%Y%m%d")
filename= os.path.join(os.getcwd(), f'log/ws_ocpp_{file}.log')
logging.basicConfig(filename=filename,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

class CentralSystem:
    def __init__(self):
        self._chargers = {}

    def get_chargers(self) -> dict:
        return self._chargers

    async def register_charger(self, cp: ChargePoint) -> asyncio.Queue:
        """ Register a new ChargePoint at the CSMS. The function returns a
        queue.  The CSMS will put a message on the queue if the CSMS wants to
        close the connection.
        """
        queue = asyncio.Queue(maxsize=1)

        # Store a reference to the task so we can cancel it later if needed.
        task = asyncio.create_task(self.start_charger(cp, queue))
        self._chargers[cp] = task
        # save
        data = {"charger_id": cp.id,
                "charge_point_model": "",
                "charge_point_vendor": ""}
        await utils.save_charger(data)

        return queue

    async def start_charger(self, cp, queue):
        """ Start listening for message of charger. """
        try:
            await cp.start()
        except Exception as e:
            print(f"Charger {cp.id} disconnected: {e}")
        finally:
            # Make sure to remove referenc to charger after it disconnected.
            del self._chargers[cp]

            # This will unblock the `on_connect()` handler and the connection
            # will be destroyed.
            await queue.put(True)

    async def change_configuration(self, key: str, value: str):
        for cp in self._chargers:
            await cp.change_configuration(key, value)

    def disconnect_charger(self, ident: str):
        for cp, task in self._chargers.items():
            if cp.id == ident:
                task.cancel()
                return

        raise ValueError(f"Charger {ident} not connected.")
