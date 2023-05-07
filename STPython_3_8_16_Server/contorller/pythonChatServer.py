from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse
import json


class CustomJSONResponse(JSONResponse):

    def __init__(self, content: any, *args, **kwargs):
        super().__init__(content, *args, **kwargs)
        self.headers["Content-Type"] = "application/json; charset=utf-8"

    def render(self, content: any) -> bytes:
        return json.dumps(content, ensure_ascii=False, allow_nan=False, indent=None, separators=(",", ":")).encode(
            "utf-8")


class PythonChatServer:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def insert_document_mongdb(self, mongoDBCtrl, collection, document):
        mongoDBCtrl.insert_document(collection, document)
        return 'success'