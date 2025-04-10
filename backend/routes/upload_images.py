import os
import tempfile
import shutil
from typing import List
from fastapi import APIRouter, UploadFile

router = APIRouter(prefix="/image_upload")


@router.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    """
    Test route for uploading multiple files.

    Returns a list of uploaded filenames to confirm receipt.
    """
    return {"filenames": [file.filename for file in files]}


@router.post("/uploadfiles/create_temp")
async def upload_and_extract(files: List[UploadFile]):
    """
    Test route to simulate saving uploaded files to a temporary directory.

    Returns both original filenames and their temporary save paths.
    """
    temp_filepaths = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for file in files:
            temp_path = os.path.join(tmpdir, file.filename)
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            temp_filepaths.append(temp_path)

        return {
            "filename": [file.filename for file in files],
            "saved_to": temp_filepaths
        }
