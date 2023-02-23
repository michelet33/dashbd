import asyncio
from ocpp.routing import on
from ocpp.v16.enums import RegistrationStatus
import logging
import websockets
# import datetime
from ocpp.v16 import call, call_result
from ocpp.v16 import ChargePoint as CP
from ocpp.v16.enums import Action
# logging.basicConfig(level=logging.DEBUG)
logging.getLogger('ocpp').setLevel(level=logging.DEBUG)
logging.getLogger('ocpp').addHandler(logging.StreamHandler())

class ChargePoint(CP):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_vendor="The Mobility House", charge_point_model= "Optimus"
        )
        response = await self.call(request)
        if response.status == RegistrationStatus.accepted:
            logging.info("Connected to central system.")

    @on(Action.UpdateFirmware)
    async def on_update_firmware(self, location:str, retries:int, retrieve_date:str, retry_interval:int):
        print(location)
        return call_result.UpdateFirmwarePayload()

async def main():
    """The charge point sends a boot notification to the central system at boot,
    in order to register itself with the central server
    The central system then responds with a confirmation.
    The trigger boot notification kickstarts this registration process
    from the central server."""
    # async with websockets.connect(
    #         'ws://localhost:8082/ocpp/CP_1',
    #         subprotocols=['ocpp1.6']
    # ) as ws:
    #     cp = ChargePoint('CP_1', ws)
    #     await asyncio.gather(cp.start(), cp.send_boot_notification())
    async with websockets.connect(
            'ws://192.168.1.129:9001/ocpp/cbid_default',
            subprotocols=['ocpp1.6']
    ) as ws:
        cp = ChargePoint('cbid_default', ws)
        await asyncio.gather(cp.start(), cp.send_boot_notification())


if __name__ == '__main__':
    asyncio.run(main())