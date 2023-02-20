# coding: utf-8
from datetime import datetime
from ocpp.routing import on
from ocpp.v16 import ChargePoint as CP
from ocpp.v16.enums import Action, RegistrationStatus, RemoteStartStopStatus
from ocpp.v16 import call_result, call


class ChargePoint16(CP):
    # def __init__(self):
    #     self._chargers = {}

    @on(Action.BootNotification)
    def on_boot_notification(self, charge_point_vendor, charge_point_model, **kwargs):
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )

    @on(Action.Heartbeat)
    def on_heartbeat(self):
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

    @on(Action.StartTransaction)
    def on_start_transaction(self, connector_id, id_tag, timestamp, meter_start, reservation_id):
        return call_result.StartTransactionPayload(
            id_tag_info={
                "status": 'Accepted'
            },
            transaction_id=int(1)
        )

    @on(Action.StopTransaction)
    def on_stop_transaction(self, transaction_id, id_tag, timestamp, meter_stop):
        return call_result.StopTransactionPayload()

    @on(Action.MeterValues)
    def on_meter_value(self):
        return call_result.MeterValuesPayload()

    @on(Action.StatusNotification)
    def on_status_notification(self, connector_id, error_code, status):
        return call_result.StatusNotificationPayload()

    @on(Action.DataTransfer)
    def on_data_transfer(self, vendor_id, message_id, data):
        return call_result.DataTransferPayload(
            status='Accepted'
        )


    def on_update_firmware(self, location, retries, retrieveDate, retryInterval):
        pass


    @on(Action.FirmwareStatusNotification)
    def on_firmware_status_notification(self, status):
        if status in (call.FirmwareStatus.downloaded, call.FirmwareStatus.downloading,
                      call.FirmwareStatus.downloadFailed, call.FirmwareStatus.idle, call.FirmwareStatus.installing,
                      call.FirmwareStatus.installation_failed, call.FirmwareStatus.installed):
            return call_result.FirmwareStatusNotificationPayload(status='Accepted')
        else:
            return call_result.FirmwareStatusNotificationPayload(status='Rejected')


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
