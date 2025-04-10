import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from .routes import module, chains, quiz,upload_images, image_chain
from .ai_workspace.agents.simple_chat.simple_chat import graph
app = FastAPI(debug=True)

# Include additional routers
app.include_router(module.router)
app.include_router(chains.router)
app.include_router(quiz.router)
app.include_router(upload_images.router)
app.include_router(image_chain.router)

# Allow CORS for your React frontend
origins = [
    "http://localhost:5173",  # Update with your frontend's origin as needed
    "http://localhost:3000",
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
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
