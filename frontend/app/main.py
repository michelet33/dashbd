from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

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
        <h1>OCPP : Send message</h1>
        <form action="" onsubmit="sendMessage(event)">
            <div class="row">
                <div class="col-sm-2">
                    <select class="form-control">
                    <option value=1 selected>1.6 JSON</option>
                    <option value=2>1.6 SOAP</option>
                    <option value=3>2.0.1 JSON</option>
                    </select>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-9">
                <div class="input-group mb-3">
                  <textarea class="form-control" placeholder="message" aria-label="Message"
                  aria-describedby="button-addon2" id="messageText" autocomplete="off"></textarea>
                  <button class="btn btn-outline-secondary" id="button-addon2">Send</button>
                </div>
                </div>
            </div>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8081/ocpp/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/central")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")