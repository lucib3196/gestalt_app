from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlmodel import Session
from ..model.question_models import Package
from ..data import question_models as service
from ..ai_workspace.agents.engineering_codegen.chains import graph, InitialMetadata, OutputState
from ..data.module import get_session

router = APIRouter(prefix="/chains")


class QueryRequest(BaseModel):
    query: str
    folder_name: str


@router.post("/", response_model=OutputState)
def run_chain(data: QueryRequest, session: Session = Depends(get_session)):
    """
    Runs the AI code generation chain with an initial metadata template,
    creates a module in the database, and returns the chain output.
    """
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
    result = graph.invoke({
        "query": data.query,
        "initial_metadata": initial_metadata
    })

    files_content = result.get("files_data")
    title = result.get("title")
    folders = [(title, files_content)]

    package = Package(title=title)
    created_package = service.create_package_with_folders(package, folders=folders,session=session)
    return result


class ChatInput(BaseModel):
    messages: list[str]
    thread_id: str


@router.post("/chat")
async def chat(input: ChatInput):
    """
    Sends a list of chat messages to the AI model and returns the final response message.
    """
    config = {"configurable": {"thread_id": input.thread_id}}
    response = await graph.ainvoke({"messages": input.messages}, config=config)
    return response["messages"][-1].content


@router.websocket("/ws/{thread_id}")
async def websocket_endpoint(websocket: WebSocket, thread_id: str):
    """
    WebSocket endpoint for streaming AI-generated messages in real-time.
    Uses a message stream with optional threading via `thread_id`.
    """
    config = {"configurable": {"thread_id": thread_id}}
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            async for event in graph.astream({"messages": [data]}, config=config, stream_mode="messages"):
                if event and len(event) > 0:
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


