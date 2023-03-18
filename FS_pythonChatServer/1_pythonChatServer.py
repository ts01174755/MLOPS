import os; import sys;
if len(sys.argv) > 1:
    os.chdir(sys.argv[1])
    sys.path.append(os.getcwd())
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import aiofiles
from FS_pythonChatServer.package.pythonChatServer import pythonChatServer
import uvicorn


if __name__ == '__main__':
    print('Here is 1_pythonChatServer.py')

    app = FastAPI()
    manager = pythonChatServer()

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                await manager.send_message(f"Client: {data}")
        except WebSocketDisconnect:
            await manager.disconnect(websocket)


    @app.get("/", response_class=HTMLResponse)
    async def get():
        async with aiofiles.open("MLOPS/FS_PythonServer/pythonChatServer/index.html", mode="r") as f:
            content = await f.read()
        return HTMLResponse(content=content)



    uvicorn.run(app, host="127.0.0.1", port=8000)
