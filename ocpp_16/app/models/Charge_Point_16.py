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
        action = ""
        if message.message_type_id==3:
            action = message.action

        data = {"charger_id": self.id,
                "message_type_id": message.message_type_id,
                "unique_id": message.unique_id,
                "action": action,
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

    @after(Action.BootNotification)
    async def after_boot_notification(self, charge_point_vendor, charge_point_model, **kwargs):
        # print(kwargs)
        if len(kwargs) > 0:
            data = kwargs
            data["firmware_version"] = data["firmwareVersion"]
            data.pop("firmwareVersion")
        data["charge_point_vendor"] = charge_point_vendor
        data["charge_point_model"] = charge_point_model
        data["charge_id"] = self.id
        await utils.save_charger(data)

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

    @after(Action.Authorize)
    async def after_authorize(self, id_tag):
        # check user price with id_tag, vendorid
        data={}
        id_token = 1
        request = call.DataTransferPayload(
            vendor_id="SetUserPrice",
            message_id=id_token,
            data=data
        )
        response = await self.call(request)


    @on(Action.DiagnosticsStatusNotification)
    async def on_diagnostics_status_notification(self, status):
        return call_result.DiagnosticsStatusNotificationPayload()
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

    @on(Action.FirmwareStatusNotification)
    async def on_firmware_status_notification(self, status):
        return call_result.FirmwareStatusNotificationPayload()

    async def send_update_firmware(self, data):
        jsondata = json.loads(data)
        request = call.UpdateFirmwarePayload(
            location=jsondata['location'],
            retries= jsondata['retries'],
            retrieve_date= jsondata['retrieveDate'],
            retry_interval = jsondata['retryInterval']
        )
        # datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') + "Z"
        logging.info(request)
        response = await self.call(request)
        d = {}
        if response:
            # for setting in response.configuration_key:
            #     print(f"{setting['key']}: {setting['value']}")
            #     d = f"{setting['key']}: {setting['value']}"
            d = response
        return d

    async def send_change_configuration(self, data):
        # print(data)
        if data is dict:
            jsondata= json.dumps(data)
        else:
            jsondata = json.loads(data)
        # print(jsondata['value'])
        request = call.ChangeConfigurationPayload(
            key=jsondata['key'],
            value=jsondata['value']
        )
        logging.info(request)
        response = await self.call(request)
        d = ""
        if response:
            d = response.status
        return d

    async def send_get_configuration(self, data):
        jsondata = json.loads(data)
        if 'key' in jsondata.keys():
            request = call.GetConfigurationPayload(
                key=jsondata['key']
            )
            logging.info(request)
            response = await self.call(request)
            d = {}
            if response:
                for setting in response.configuration_key:
                    print(f"{setting['key']}: {setting['value']}")
                    d = {'charger_id': self.id,'connectors':setting['value']}
                await utils.save_charger(d)
            return d
        else:
            logging.error(f"No attribut 'key' in : {jsondata}")

    async def send_remote_start_transaction(self, data):
        jsondata = json.loads(data)
        request = call.RemoteStartTransactionPayload(
            connector_id=jsondata['connectorId'],
            id_tag=jsondata['IdTag']
        )
        response = await self.call(request)
        if response.status == RemoteStartStopStatus.accepted:
            print("Transaction Started!!!")
        return response

    async def send_remote_stop_transaction(self, data):
        jsondata = json.loads(data)
        request = call.RemoteStopTransactionPayload(
            transaction_id=jsondata['transactionId']
        )
        response = await self.call(request)

        if response.status == RemoteStartStopStatus.accepted:
            print("Stopping transaction")
        return response
    async def send_reset(self, data):
        jsondata = json.loads(data)
        if jsondata['type'] in ('Hard', 'Soft'):
            print('--reset : ' + jsondata['type'])
            return call.ResetPayload(
                type=jsondata['type']
            )
            response = await self.call(request)

            print('--reset : ' + jsondata['type'])
            return response
        else:
            logging.error(f"type is not Hard or Soft: {jsondata['type']}")
            return f"type is not Hard or Soft: {jsondata['type']}"

    async def send_get_diagnostics(self, data):
        print(data)
        jsondata = json.loads(data)
        request = call.GetDiagnosticsPayload(
            location=jsondata['location']
            , retries=jsondata['retries']
            , retry_interval=jsondata['retryInterval']
            , start_time=jsondata['startTime']
            , stop_time=jsondata['stopTime']
        )
        d = ""
        try:
            response = await self.call(request)
            if response:
                d = f"'fileName':'{response.file_name}'"
        except Exception:
            d="error on response"
        finally:
            return d
