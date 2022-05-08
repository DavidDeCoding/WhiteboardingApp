from typing import Optional, List

from fastapi import Cookie, Depends, FastAPI, Query, WebSocket, status, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Chat</title>
        </head>
        <body>
            <h1>WebSocket Chat</h1>
            <form action="" onsubmit="sendMessage(event)">
                <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
                <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
                <h2>Your ID: <span id="ws-id"></span></h2>
                <button onclick="connect(event)">Connect</button>
                <hr>
                <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
                <button>Send</button>
            </form>
            <ul id='messages'>
            </ul>
            <script>
            var ws = null;
                function connect(event) {
                    var itemId = document.getElementById("itemId")
                    var token = document.getElementById("token")
                    var client_id = Date.now()
                    document.querySelector("#ws-id").textContent = client_id;
                    ws = new WebSocket(`ws://localhost:8000/items/${itemId.value}/${client_id}/ws?token=${token.value}`);
                    ws.onmessage = function(event) {
                        var messages = document.getElementById('messages')
                        var message = document.createElement('li')
                        var content = document.createTextNode(event.data)
                        message.appendChild(content)
                        messages.appendChild(message)
                    };
                    event.preventDefault()
                }
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


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)


async def get_cookie_or_token(
        websocket: WebSocket,
        session: Optional[str] = Cookie(None),
        token: Optional[str] = Query(None)
):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@app.websocket("/items/{item_id}/{client_id}/ws")
async def websocket_endpoint(
        websocket: WebSocket,
        item_id: str,
        client_id: int,
        q: Optional[int] = None,
        cookie_or_token: str = Depends(get_cookie_or_token)
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Session cookie or query token value is: {cookie_or_token}", websocket)
            if q is not None:
                await manager.send_personal_message(f"Query parameter q is: {q}", websocket)
            await manager.send_personal_message(f"You wrote: {data}, for Item ID: {item_id}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}, for Item ID: {item_id}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
