from fastapi import FastAPI, Request
import uvicorn


app = FastAPI()

app.get("/")
async def root():
    return {"message": "Processing data"}

@app.post("/position_send")
async def show_position(request: Request):
    position_tick = await request.json()
    return {"data": position_tick}

@app.get("/position")
async def show_position(request: Request):
    position_tick = await request.json()
    return {"data": position_tick}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
