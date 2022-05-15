from fastapi import WebSocket, FastAPI
from typing import List


class HandleMutiConnection:
    def __init__(self):
        self.connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)
        
    async def send_data(self, websocket: WebSocket, data: str):
        await websocket.send_text(data)
    
    async def broadcast_data(self, data: str):
        for websocket in self.connections:
            await websocket.send_text(data)