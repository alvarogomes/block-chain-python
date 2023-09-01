import time
from threading import Thread
from fastapi import WebSocket


class Manager:
    def __init__(self):
        self.workers = []
        self.leader = None
        self.check_thread = Thread(target=self.check_leader)
        self.check_thread.start()

    def register(self):
        new_id = len(self.workers) + 1
        self.workers.append(new_id)
        if self.leader is None:
            self.leader = new_id
        return new_id

    def get_workers(self, new_id):
        return [item for item in self.workers if item != new_id]

    def get_leader(self):
        return self.leader

    async def connect_client(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.connections[client_id] = websocket
        try:
            while True:
                data = await websocket.receive_text()
                # Broadcast da mensagem para todos os outros clientes conectados
                for client, ws in self.connections.items():
                    if client != client_id:
                        await ws.send_text(data)
        except:
            del self.connections[client_id]

    def check_leader(self):
        while True:
            time.sleep(20)
            # Checar se o líder ainda está ativo
            if self.leader not in self.workers:
                self.leader = self.workers[0] if self.workers else None
