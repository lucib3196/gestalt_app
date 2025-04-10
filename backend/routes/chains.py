from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from sqlmodel import Session
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from ..ai_workspace.agents.simple_chat_stream import main as stream
from fastapi import APIRouter, Query
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from ..model.module_db import Module, Folder, File, ModuleSimple
from ..data import module as service
from ..ai_workspace.agents.engineering_codegen.chains import graph, OverallState, InitialMetadata, OutputState
from ..data.module import get_session
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse



router = APIRouter(prefix="/chains")

class QueryRequest(BaseModel):
    query: str
    folder_name: str


@router.post("/", response_model=OutputState)
def run_chain(data: QueryRequest, session: Session = Depends(get_session)):
    
    # Step 0 Initialize Metadata (this shoudl be changed eventually)
    metadata_dict = {
        "createdBy": "lberm007@ucr.edu",
        "qtype": "num",
        "nSteps": 1,
        "updatedBy": "",
        "difficulty": 1,
        "codelang": "javascript",
        "reviewed": "False",
        "ai_generated": "True"
    }
    initial_metadata = InitialMetadata(**metadata_dict)
    # Step 1: Run AI chain
    result = graph.invoke({"query": data.query,"initial_metadata":initial_metadata })
    
    files_content = result.get("files_data")
    title = result.get("title")
    folders = [(title, files_content)]
    
    # Step 3: Create folder and files
    module = ModuleSimple(name=title)
    created_module = service.create_module(module, folders = folders, session=session)
    return result





# Not Ready actively working on 
class ChatInput(BaseModel):
    messages:list[str]
    thread_id: str
    
@router.post("/chat")
async def chat(input:ChatInput):
    config = {"configurable": {"thread_id": input.thread_id}}
    response = await graph.ainvoke({"messages": input.messages}, config=config)
    return response["messages"][-1].content
    
    
# Streaming
@router.websocket("/ws/{thread_id}") 
async def websocket_endpoint(websocket:WebSocket, thread_id:str):
    config = {"configurable": {"thread_id": thread_id}}
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            async for event in graph.astream({"messages": [data]}, config=config, stream_mode="messages"):
                if event and len(event)>0:
                    message_content = event[0].content
                    await websocket.send_json({
                        "content": message_content,
                        "isComplete": False
                    })
            await websocket.send_json({
                "content": "",
                "isComplete": True
            })
    except WebSocketDisconnect:
        print(f"Client disconnected from thread {thread_id}")
    except Exception as e:
        print(f"Error in WebSocket: {str(e)}")
        await websocket.close(code=1011)  # Internal error
        