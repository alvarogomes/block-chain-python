from fastapi import FastAPI, WebSocket
from manager import Manager
import uvicorn

app = FastAPI()
manager = Manager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect_client(websocket, client_id)


@app.post("/register")
async def register_worker():
    worker_id = manager.register()
    return {"worker_id": worker_id}


@app.post("/check_leader")
async def check_leader():
    return {"leader": manager.get_leader()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=18000)
