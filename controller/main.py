from fastapi import FastAPI, Request, BackgroundTasks
import json
from utils import Controller
from sklearn.preprocessing import normalize
import asyncio
import uvicorn


app = FastAPI()
controller = Controller()


@app.on_event('startup')
async def run_works():
    asyncio.create_task(controller.run_works())

@app.on_event('startup')
async def send_position():
    asyncio.create_task(controller.send_data())


@app.get("/")
async def root():
    return {"message": "Processing data"}

@app.post("/fill")
async def update_fill(request: Request):
    try:
        fill_tick = await request.json()
        controller.add_work(fill_tick)
        message = "Success"
    except json.JSONDecodeError:
        fill_tick = None
        message = "Received data is not a valid JSON"
    return {"message": message, "received_data_as_json": fill_tick}


@app.post("/aum")
async def update_aum(request: Request):
    try:
        aum_splits_json = await request.json()
        controller.accounts_split = aum_splits_json
        controller.accounts_split_norm = controller.normalize_dict(aum_splits_json)
        message = "Success"
    except json.JSONDecodeError:
        aum_splits_json = None
        message = "Received data is not a valid JSON"
    return {"message": message, "received_data_as_json": aum_splits_json}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

