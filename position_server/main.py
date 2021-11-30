from fastapi import FastAPI, Request
import uvicorn
import datetime


app = FastAPI()

app.get("/")
async def root():
    return {"message": "Processing data"}

@app.post("/position_send")
async def show_position(request: Request):
    position_tick = await request.json()
    print(f"New positions coming to position server are: {datetime.datetime.now()}: {position_tick}")
    return {"data": position_tick}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
