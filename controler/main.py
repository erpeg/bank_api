from fastapi import FastAPI, Request
from json import JSONDecodeError
from . import schemas

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/aum")
async def create_avm(request: Request):
    try:
        payload_as_json = await request.json()
        print(payload_as_json)
        message = "Success"
    except JSONDecodeError:
        payload_as_json = None
        message = "Received data is not a valid JSON"
    return {"message": message, "received_data_as_json": payload_as_json}
