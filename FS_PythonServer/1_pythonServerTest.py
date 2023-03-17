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
    print('Here is 1_pythonServerTest.py')

    app = FastAPI()

    app.mount("/File", StaticFiles(directory="MLOPS/FS_PythonServer/File"), name="File")

    templates = Jinja2Templates(directory="templates")

    # @app.get("/")
    # async def root():
    #     return {"message": "Hello World"}
    #
    # @app.get("/items/{item_id}")
    # async def read_item(item_id: int, q: str = None):
    #     return {"item_id": item_id, "q": q}

    @app.get("/", response_class=HTMLResponse)
    async def read_index(request: Request):
        # return "Hello World"
        return templates.TemplateResponse("index.html", {"request": request})

    uvicorn.run(app, host="127.0.0.1", port=8000)
