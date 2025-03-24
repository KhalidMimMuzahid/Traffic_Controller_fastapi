from fastapi import FastAPI , Depends,  WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routes.router import router
from database import init_db
from typing import List
from exceptions.handler import register_all_errors
from dependencies.authenticate_user import authenticate_user
from websocket import active_connections
import json
import asyncio
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# # If you want to automatically initialize your DB on startup,
# @app.on_event("startup")
# async def on_startup():
#     # This will run when the application starts and use the existing event loop.
#     await init_db()



# Store active WebSocket connections
# active_connections: List[WebSocket] = []

# WebSocket Endpoint - Any user can connect
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print(f"✅ New client connected. Total connections: {len(active_connections)}")

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)  # Parse received JSON
            event = message.get("event")
            payload = message.get("data")

            print(f"📩 Received event: {event}, data: {payload}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)  # Remove disconnected client
        print(f"❌ Client disconnected. Total connections: {len(active_connections)}")



# we are redirecting all routes to routes to handle easily
app.include_router(router, prefix="/api/v1", dependencies=[Depends(authenticate_user)])

register_all_errors(app)






# API to broadcast messages to all users
@app.get("/broadcast/{message}")
async def broadcast_event(message: str):
    event_message = json.dumps({"event": "emit001", "data": message})

    if active_connections:
        await asyncio.gather(*(ws.send_text(event_message) for ws in active_connections))

    return {"status": "Broadcast sent", "message": message}






