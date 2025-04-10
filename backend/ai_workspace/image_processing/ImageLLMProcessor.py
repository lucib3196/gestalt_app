from dataclasses import dataclass, field
from venv import create
from langchain import hub
from typing import Union, Optional,List
from langchain_core.prompts.chat import ChatPromptTemplate

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import asyncio
import base64
from langchain_core.messages import HumanMessage
from typing import Optional, Type

async def encode_image(image_path:str)->str:
    try:
        with open(image_path,'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
        raise
async def encode_multiple_images(image_paths:List[str])->List[str]: # type: ignore
    try: 
        return await asyncio.gather(*(encode_image(image_path) for image_path in image_paths))
    except Exception as e:
        print(f'Error Encoding multiple images. Error : {e} ')
async def create_image_content_payload(image_paths:List[str])->List[dict]:
    encoded_images = await encode_multiple_images(image_paths)
    image_contents = [
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image}",
                "detail": "high"
            }
        }
        for image in encoded_images
    ]
    return image_contents


@dataclass
class ImageLLMProcessor:
    """
    A processor for handling image-based payloads and sending structured requests
    to an LLM with optional schema validation.
    
    Attributes:
        prompt: The prompt string or ChatPromptTemplate for the LLM.
        schema: An optional Pydantic model for validating structured responses.
        model: The name of the LLM model to use (e.g., 'gpt-4o').
    """
    prompt: Union[str, ChatPromptTemplate]
    schema: Optional[Type[BaseModel]] = None
    model: str = "gpt-4o"

    def __post_init__(self):
        self.llm = ChatOpenAI(model=self.model)
        if self.schema is not None:
            self.llm = self.llm.with_structured_output(self.schema)
        # type: ignore
        self.processed_prompt = (
            self.prompt.messages[0].prompt.template  # type: ignore
            if isinstance(self.prompt, ChatPromptTemplate)
            else self.prompt
        )

    async def send_arequest_stream(
        self, image_paths: list[str], delimiter: str = "content") -> Optional[dict]:
        """
        Sends a request to the LLM with image data and streams the response.

        Args:
            image_paths: A list of file paths to the images.
            delimiter: The key used to extract content from the streamed chunks.

        Returns:
            None if successful (streaming handled), or a dictionary with an error message if it fails.
        """
        try:
            # Prepare the message for the LLM
            message = await self.prepare_message(image_paths)

            # Initialize a list to collect streamed chunks (optional use case)
            chunks = []

            # Process streamed chunks from the LLM
            async for chunk in self.llm.astream([message]):
                if isinstance(chunk, dict) and delimiter in chunk:
                    content = chunk[delimiter]
                    chunks.append(content)  # Optional: Collect streamed content
                    print(content, flush=True)  # Print to console (stream output)
                
                # Not Correctly Implemented
                elif isinstance(chunk,BaseModel):
                    if hasattr(chunk,delimiter):
                        content = getattr(chunk, delimiter)
                        chunks.append(content)
                        print(getattr(chunk, delimiter), end="|", flush=True)
                    else:
                        print(f"Delimiter '{delimiter}' not found in {chunk.__class__.__name__}. Available fields: {chunk.dict().keys()}", flush=True)
                else:
                    # Handle unexpected chunk structure
                    print(f"Unexpected chunk format: {type(chunk)}", flush=True)

            return None  # Streaming complete

        except Exception as e:
            # Log the error and return a response
            print(f"Error streaming image request: {e}", flush=True)
            return {"error": str(e)}
    
    
    async def send_arequest(self,image_paths:list[str]):
        try: 
            message = await  self.prepare_message(image_paths)
            response = await self.llm.ainvoke([message])
            return response.dict() # type: ignore
        except Exception as e:
            print(f"Error sending image request: {e}")
            return {"error": str(e)}
            
    
    async def prepare_message(self,image_paths:list[str]):
        try:
            self.validate_inputs(image_paths)
            image_contents = await create_image_content_payload(image_paths)
            message = HumanMessage(
                content=[
                    {"type": "text", "text": self.processed_prompt},  # type: ignore
                    *image_contents,
                ],
            )
        except Exception as e:
            print(f"Error preparing message: {e}")
            return {"error": str(e)}
        return message
        
    def validate_inputs(self, image_paths: list[str]):
        """
        Validates the input arguments for the request.

        Args:
            image_paths: A list of file paths to the images.

        Raises:
            ValueError: If the list of image paths is empty.
            TypeError: If the prompt is of an invalid type.
        """
        if not image_paths:
            raise ValueError("The image_paths list cannot be empty.")
        if not isinstance(self.prompt, (str, ChatPromptTemplate)):
            raise TypeError("Prompt must be either a string or a ChatPromptTemplate.")
    
    
