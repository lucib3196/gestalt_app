import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from .web import module
from .ai_workspace.agents.simple_chat.simple_chat import graph

app = FastAPI(debug=True)

# Include additional routers
app.include_router(module.router)

# Allow CORS for your React frontend
origins = [
    "http://localhost:5173",  # Update with your frontend's origin as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the input for chat
class ChatInput(BaseModel):
    messages: List[str]
    thread_id: str

# REST endpoint for chat requests
@app.post("/chat")
async def chat(input: ChatInput):
    config = {"configurable": {"thread_id": input.thread_id}}
    response = await graph.ainvoke({"messages": input.messages}, config=config)
    return response["messages"][-1].content

# WebSocket endpoint for streaming chat messages
@app.websocket("/ws/{thread_id}")
async def websocket_endpoint(websocket: WebSocket, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        async for event in graph.astream({"messages": [data]}, config=config, stream_mode="messages"):
            await websocket.send_text(event[0].content)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
