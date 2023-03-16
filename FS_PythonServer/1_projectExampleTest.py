import os; import sys;
if len(sys.argv) > 1:
    os.chdir(sys.argv[1])
    sys.path.append(os.getcwd())
from fastapi import FastAPI
import uvicorn


if __name__ == '__main__':
    print('Here is 1_projectExampleTest.py')

    app = FastAPI()
    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.get("/items/{item_id}")
    async def read_item(item_id: int, q: str = None):
        return {"item_id": item_id, "q": q}

    uvicorn.run(app, host="127.0.0.1", port=8000)