# coding: utf-8
import os.path
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from fastapi import Response
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOGIN_ENDPOINT = "http://192.168.1.129:5000/"


@app.get("/central")
async def get_html():
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <script
              src="https://code.jquery.com/jquery-3.6.3.js"
              integrity="sha256-nQLuAZGRRcILA+6dMBOvcRh5Pe310sBpanc6+QBmyVM="
              crossorigin="anonymous"></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
            <title>Backend Ocpp</title>
        </head>
        <body class="container">
            <div class="row mb-3"><h1>Test envoi message OCPP</h1></div>
            <div class="row">
            <form action="" onsubmit="sendMessage(event)" class='mt-3 pt-3'>
                <div class='row'>
                    <div class="col-sm-3">
                        <label for="SelectRequest" class="form-label">Station *</label>
                        <select class="form-control" value="" id='Stationid' name="SelectCharger" required>
                        {list_chargers}
                        </select>
                    </div>
                     <div class="col-sm-3">
                        <label for="SelectProtocol" class="form-label">Version protocole</label>
                        <select class="form-control" value="" id='Protocol' name="SelectProtocol">
                        <option value='ocpp1.6' selected>1.6 JSON</option>
                        <option value='ocpp2.0.1'>2.0.1 JSON</option>
                        </select>
                    </div>
                     <div class="col-sm-6"></div>
                </div>
                <hr />
                <div class="row">
                    <div class="col-sm-3">
                        <label for="SelectRequest" class="form-label">Type de requête *</label>
                        <select class="form-control" value="" id='RequestType' name="SelectRequest" required>
                        {list_requests}
                        </select>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm-9">
                    <label for="RequestContent" class="form-label">Message json *</label>
                      <textarea class="form-control" placeholder="message" aria-label="Message" name='RequestContent'
                      aria-describedby="button-addon2" id="messageText" autocomplete="off" required></textarea>
                      <button class="btn btn-outline-secondary" id="btnSend">Envoyer</button>
                    </div>
                </div>
            </form>
            </div>
            <ul id='messages'>
            </ul>
            <script>
                var protocol = document.getElementById("Protocol").value;
                var ws = new WebSocket("ws://192.168.1.129:9001/ws", subprotocols=[protocol]);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages');
                    var message = document.createElement('li');
                    var content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);
                };
                function sendMessage(event) {
                    var stationid = document.getElementById("Stationid").value;
                    var req = document.getElementById("RequestType").value;
                    var input = document.getElementById("messageText");
                    var data = {};
                    data["action"]=req;
                    data["content"]=input.value;
                    data["charger"]=stationid;
                    // data["protocol"]=protocol;
                    console.log(data);
                    ws.send(JSON.stringify(data));
                    input.value = '';
                    event.preventDefault();
                }
                
                var selectElement = document.getElementById("Protocol");
                
                selectElement.addEventListener("change", (event) => {
                  var selectobject = document.getElementById("RequestType");
                  var nb = selectobject.length
                  while (selectobject.options.length > 0) {
                        selectobject.remove(0);
                    }
                  let newOption = new Option('','');
                  selectobject.add(newOption,undefined);
                  
                });
                
            </script>
        </body>
    </html>
    """
    try:
        # the following line is responsible for suppressing the warning.
        url = os.path.join(LOGIN_ENDPOINT, 'chargers/get/')
        requests.packages.urllib3.disable_warnings()
        response = requests.get(
            url=url,
            timeout=30,
            verify=False
        )
        response.raise_for_status()
        # print(response.content)
        dic = response.json()
        chargers = [f"<option value='{c['charger_id']}'>{c['charger_id']}</option>" for c in dic]
        chargers.insert(0, '<option value=''></option>')
        list_chargers = ' '.join(chargers)
        # print(list_chargers)

        url = os.path.join(LOGIN_ENDPOINT, 'ocpp/requests/get/')
        response = requests.get(
            url=url,
            timeout=30,
            verify=False
        )
        response.raise_for_status()
        # print(response.content)
        dic = response.json()
        req = [f"<option value='{c['name']}'>{c['name']}</option>" for c in dic]
        req.insert(0, '<option value=''></option>')
        list_requests = ' '.join(req)
        # print(list_requests)
        html = html.replace(" {list_chargers}",list_chargers)
        html = html.replace("{list_requests}",list_requests)
    except requests.HTTPError as error:
        return Response(
            status_code=error.response.status_code
        )
    return HTMLResponse(html)
