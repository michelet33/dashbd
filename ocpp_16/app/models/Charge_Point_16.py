# coding: utf-8
import json
import os
from datetime import datetime
from ocpp.routing import on, after
from ocpp.v16 import ChargePoint as CP
from ocpp.v16.enums import Action, RegistrationStatus, RemoteStartStopStatus
from ocpp.v16 import call_result, call
from ocpp.messages import unpack
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

class ChargePoint16(CP):
    # def __init__(self):
    #     self._chargers = {}

    async def route_message(self, raw_msg):
        # super of function route_message in order to get unique id
        await super().route_message(raw_msg)
        # print(raw_msg)
        message = unpack(raw_msg)
        data = {"charger_id": self.id,
                "message_type_id": message.message_type_id,
                "unique_id": message.unique_id,
                "action": message.action,
                "content": str(message.payload)}
        await utils.save_log(data)

    async def _send(self, message):
        await super()._send(message)
        msg = unpack(message)
        data = {"charger_id": self.id,
                "message_type_id": msg.message_type_id,
                "unique_id": msg.unique_id,
                "action": msg.action,
                "content": str(msg.payload)}
        await utils.save_log(data)
    @on(Action.BootNotification)
    async def on_boot_notification(self, charge_point_vendor, charge_point_model, **kwargs):
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )

    # @after(Action.BootNotification)
    # async def after_boot_notification(self, charge_point_vendor, charge_point_model, **kwargs):
    #     data = {"charger_id": self.id,
    #      "action": "BootNotification",
    #      "content": "{'charge_point_vendor': '"+charge_point_vendor+"', 'charge_point_model': '"+charge_point_model+"'}"
    #             }
    #     await utils.save_log(data)

    @on(Action.Heartbeat)
    async def on_heartbeat(self):
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') + "Z"
        )

    @on(Action.Authorize)
    async def on_authorize(self, id_tag):
        # return call_result.AuthorizePayload(id_token_info={"status": AuthorizationStatusType.accepted})
        return call_result.AuthorizePayload(
            id_tag_info={
                "status": "Accepted"
            }
        )
    # @after(Action.Authorize)
    # async def after_on_authorize(self, id_tag):
    #     data = {"charger_id": self.id,
    #             "action": "Authorize",
    #             "content": "{'idtag': '" + id_tag + "'}"}
    #     await utils.save_log(data)

    @on(Action.StartTransaction)
    async def on_start_transaction(self, connector_id, id_tag, timestamp, meter_start, reservation_id):
        return call_result.StartTransactionPayload(
            id_tag_info={
                "status": 'Accepted'
            },
            transaction_id=int(1)
        )

    @on(Action.StopTransaction)
    async def on_stop_transaction(self, transaction_id, id_tag, timestamp, meter_stop):
        return call_result.StopTransactionPayload()

    @on(Action.MeterValues)
    async def on_meter_value(self):
        return call_result.MeterValuesPayload()

    @on(Action.StatusNotification)
    async def on_status_notification(self, connector_id, error_code, status,timestamp, **kwargs):
        return call_result.StatusNotificationPayload()

    @on(Action.DataTransfer)
    async def on_data_transfer(self, vendor_id, message_id, data):
        return call_result.DataTransferPayload(
            status='Accepted'
        )

    async def send_update_firmware(self, data):
        jsondata = json.loads(data)
        request = call.UpdateFirmwarePayload(
            location=jsondata['location'],
            retries= jsondata['retries'],
            retrieve_date= jsondata['retrieveDate'],
            retry_interval = jsondata['retryInterval']
        )
        # datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') + "Z"
        logging.info('UPDATE FIRMWARE step 2')
        logging.info(request)
        await self.call(request)
        # if response.status == RegistrationStatus.accepted:
        # logging.info("Update firmware accepted")
        #
        # data = {"charger_id": self.id,
        #         "action": "UpdateFirmware",
        #         "content": "{'location': '"+ str(jsondata['location']) +"', 'retries': "+
        #                    str(jsondata['retries'])+", 'retrieveDate':'"+str(jsondata['retrieveDate'])+
        #                    "', 'retryInterval':"+str(jsondata['retryInterval'])+"}"}
        # await utils.save_log(data)

    @on(Action.FirmwareStatusNotification)
    async def on_firmware_status_notification(self, status):
        return call_result.FirmwareStatusNotificationPayload()

    # @after(Action.FirmwareStatusNotification)
    # async def after_firmware_status_notification(self, status):
    #     # print(self.call.unique_id)
    #     data = {"charger_id": self.id,
    #             "unique_id": '',
    #             "action": "FirmwareStatusNotification",
    #             "content": "{'status': '" + str(status) + "'}"}
    #     await utils.save_log(data)
    async def remote_start_transaction(self):
        request = call.RemoteStartTransactionPayload(
            id_tag='1'
        )
        response = await self.call(request)
        if response.status == RemoteStartStopStatus.accepted:
            print("Transaction Started!!!")

    async def remote_stop_transaction(self):
        request = call.RemoteStopTransactionPayload(
            transaction_id=1
        )
        response = await self.call(request)

        if response.status == RemoteStartStopStatus.accepted:
            print("Stopping transaction")
