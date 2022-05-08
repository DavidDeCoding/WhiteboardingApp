from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Chat</title>
        </head>
        <body>
            <h1>Websocket Chat</h1>
            <form action="" onSubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off"/>
            </form>
            <ul id="messages">
            </ul>
            <script>
                const ws = new WebSocket("ws://localhost:8000/ws");
                ws.onmessage = function(event) {
                    const messages = document.getElementById("messages");
                    const message = document.createElement("li");
                    const content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);
                };
                
                function sendMessage(event) {
                    var input = document.getElementById("messageText");
                    ws.send(input.value);
                    input.value = "";
                    event.preventDefault();
                }
            </script>
        </body>
    </html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
