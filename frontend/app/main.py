# coding: utf-8
# import os
# from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
# import logging


# now = datetime.now()
# file = now.strftime("%Y%m%d")
# filename= os.path.join(os.getcwd(), f'log/ws_ocpp_{file}.log')
# logging.basicConfig(filename=filename,
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.DEBUG)

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous">
        </script>
        <title>Backend Ocpp</title>
    </head>
    <body class="container">
        <h1>Send message OCPP</h1>
        <form action="" onsubmit="sendMessage(event)">
            <div class="row">
                <div class="col-sm-2">
                    <label for="SelectProtocol" class="form-label">Version protocole</label>
                    <select class="form-control" id='protocol' name="SelectProtocol">
                    <option value='ocpp1.6' selected>1.6 JSON</option>
                    <option value='ocpp2.0.1'>2.0.1 JSON</option>
                    </select>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-2">
                    <label for="SelectRequest" class="form-label">Type de requête *</label>
                    <select class="form-control" value=0 id='RequestType' name="SelectRequest" required>
                    <option value="" selected></option>
                    <option value="UpdateFirmware">UpdateFirmware</option>
                    <option value="SendLocalList">SendLocalList</option>
                    <option value="GetLocalList">GetLocalList</option>
                    <option value="RemoteStartTransaction">RemoteStartTransaction</option>
                    <option value="RemoteStopTransaction">RemoteStopTransaction</option>
                    <option value="CancelReservation">CancelReservation</option>
                    <option value="ChangeAvailability">ChangeAvailability</option>
                    <option value="ChangeConfiguration">ChangeConfiguration</option>
                    <option value="ClearCache">ClearCache</option>
                    <option value="ClearChargingProfile">ClearChargingProfile</option>
                    <option value="DataTransfer">DataTransfer</option>
                    <option value="GetCompositeSchedule">GetCompositeSchedule</option>
                    <option value="GetConfiguration">GetConfiguration</option>
                    <option value="GetDiagnostics">GetDiagnostics</option>
                    <option value="GetLocalListVersion">GetLocalListVersion</option>
                    <option value="ReserveNow">ReserveNow</option>
                    <option value="Reset">Reset</option>
                    <option value="StartTransaction">StartTransaction</option>
                    <option value="StopTransaction">StopTransaction</option>
                    <option value="TriggerMessage">TriggerMessage</option>
                    <option value="UnlockConnector">UnlockConnector</option>
                    </select>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-9">
                <label for="RequestContent" class="form-label">Message json *</label>
                  <textarea class="form-control" placeholder="message" aria-label="Message" name='RequestContent'
                  aria-describedby="button-addon2" id="messageText" autocomplete="off" required></textarea>
                  <button class="btn btn-outline-secondary" id="button-addon2">Envoyer</button>
        
                </div>
            </div>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://192.168.1.129:9001/ws", subprotocols=['ocpp1.6']);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
            };
            function sendMessage(event) {
                var req = document.getElementById("RequestType").value;
                var input = document.getElementById("messageText");
                var data = {};
                data["action"]=req;
                data["content"]=input.value;
                data["charger"]='cbid_default';
                console.log(data);
                ws.send(JSON.stringify(data));
                input.value = '';
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""

@app.get("/central")
async def get():
    return HTMLResponse(html)
