from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from functions import  slack_assistant


app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()



@app.websocket("/ws/network")
async def websocket_network(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            response = slack_assistant(data)
            await manager.send_personal_message(response['text'], websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)




@app.websocket("/ws/line_of_business")
async def websocket_line_of_business(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Line of Business: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

 

@app.websocket("/ws/finance")
async def websocket_finance(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Finance: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# new socket for operations
@app.websocket("/ws/operations")
async def websocket_operations(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Operations: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# new  socket for marketing
@app.websocket("/ws/marketing")
async def websocket_marketing(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Marketing: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# new socket for hr
@app.websocket("/ws/hr")
async def websocket_hr(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"HR: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agents_app:app", host="0.0.0.0", port=9876, reload=True)