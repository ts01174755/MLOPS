import os; import sys;
if len(sys.argv) > 1:
    os.chdir(sys.argv[1])
    sys.path.append(os.getcwd())
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn


if __name__ == '__main__':
    print('Here is 1_pythonChatServer.py')

    app = FastAPI()

    app.mount("/File", StaticFiles(directory="MLOPS/FS_PythonServer/File"), name="File")

    templates = Jinja2Templates(directory="MLOPS/FS_PythonServer/File/templates")

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.get("/items/{id}", response_class=HTMLResponse)
    async def read_item(request: Request, id: str):
        return templates.TemplateResponse("item.html", {"request": request, "id": id})

    uvicorn.run(app, host="127.0.0.1", port=8000)
