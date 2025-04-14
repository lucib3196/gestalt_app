# Standard Library Imports
import os
import io
import json
import tempfile
import zipfile
from typing import List, Tuple, Dict, Any, Optional
from io import BytesIO

# Third-Party Imports
from fastapi import HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from sqlmodel import Session, select

# Internal App Imports
from .database import engine
from .helpers import create_zip_file
from ..model.module_db import Module, Folder, File, ModuleSimple


# This should be fixed eventually to be included in the database
file_name_map: dict[str, str] = {
    "question_txt": "question.txt",
    "question_html": "question.html",
    "server_js": "server.js",
    "server_py": "server.py",
    "solution_html": "solution.html",
    "metadata": "info.json",
}


# Current Working Version With Simple Module


def get_module_folders(module_id: int, session: Session) -> List[Folder]:
    """
    Fetch all folders belonging to a given module.
    Raises a 404 error if the module or folders don't exist.
    """
    module = session.get(ModuleSimple, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    folders = session.query(Folder).filter_by(module_id=module_id).all()
    if not folders:
        raise HTTPException(status_code=404, detail="No folders found for this module")

    return folders


def get_folder_files(module_id: int, folder_id: int, session: Session) -> List[File]:
    """
    Fetch all files in a specific folder within a given module.
    Validates both module and folder existence and their relationship.
    """
    # Ensure folder exists and belongs to the given module
    folder = session.query(Folder).filter_by(id=folder_id, module_id=module_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found for this module")

    return folder.files


def get_all_folders(session: Session)->List[Folder]:
    folders = session.exec(select(Folder)).all()
    return folders



def download_single_folder(module_id: int, folder_id: int, session: Session):

    folder: Folder = (
        session.query(Folder).filter_by(id=folder_id, module_id=module_id).first()
    )
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found for this module")
    folder_name = folder.name
    folder_files: List[File] = folder.files
    temp_filepaths = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for file in folder_files:
            tempfile_path = os.path.join(
                tmpdir,
                (
                    file.save_name
                    if file.save_name is not None
                    else file_name_map.get(file.name)
                ),
            )
            content = file.content
            if isinstance(content, str):
                content = content.encode("utf-8")
            elif isinstance(content, dict):
                content = json.dumps(content)

            with open(tempfile_path, "wb") as f:
                f.write(content)

            temp_filepaths.append(tempfile_path)
        zip_stream = create_zip_file(temp_filepaths)
        headers = {"Content-Disposition": f"attachment; filename={folder_name}.zip"}
        return StreamingResponse(
            zip_stream, media_type="application/zip", headers=headers
        )






def download_all_folders_in_module(module_id: int, session: Session):
    """
    Downloads a ZIP containing all folders associated with the specified module.
    Each folder is zipped individually and combined into a master ZIP.
    """
    folders: List[Folder] = (
        session.query(Folder).filter(Folder.module_id == module_id).all()
    )

    if not folders:
        raise HTTPException(status_code=404, detail="No folders found for this module.")

    master_zip_buffer = BytesIO()

    with zipfile.ZipFile(master_zip_buffer, "w", zipfile.ZIP_DEFLATED) as master_zip:
        for folder in folders:
            folder_name = folder.name
            folder_id = folder.id
            folder_files: List[File] = folder.files

            folder_zip_buffer = BytesIO()

            with zipfile.ZipFile(
                folder_zip_buffer, "w", zipfile.ZIP_DEFLATED
            ) as folder_zip:
                for file in folder_files:
                    filename = file.save_name or file_name_map.get(file.name, file.name)
                    content = file.content

                    if isinstance(content, str):
                        content = content.encode("utf-8")
                    elif isinstance(content, dict):
                        content = json.dumps(content).encode("utf-8")

                    folder_zip.writestr(filename, content)

            folder_zip_buffer.seek(0)
            master_zip.writestr(
                f"{folder_name}_{folder_id}.zip", folder_zip_buffer.read()
            )

    master_zip_buffer.seek(0)
    headers = {
        "Content-Disposition": f"attachment; filename=module_{module_id}_folders.zip"
    }

    return StreamingResponse(
        master_zip_buffer, media_type="application/zip", headers=headers
    )


# These are a bit older and still work however i need to eventually move them and improve them


def get_module_id(module_id: int, session: Session = None) -> ModuleSimple:
    module = session.get(ModuleSimple, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


def get_module_folder(module_id: int, session: Session = None) -> Folder:
    folder = session.query(Folder).filter_by(module_id=module_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder


def get_module_files(module_id: int, session: Session) -> List[File]:
    folder = session.query(Folder).filter_by(module_id=module_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder.files  # Assumes relationship Folder.files is defined.


def get_modules_simple(
    skip: int = 0, limit: int = 10, session: Session = None
) -> List[ModuleSimple]:
    return session.exec(select(ModuleSimple).offset(skip).limit(limit)).all()


def get_single_file(module_id: int, file_id: int, session: Session) -> str:
    file = (
        session.query(File)
        .join(Folder, File.folder_id == Folder.id)
        .filter(File.id == file_id, Folder.module_id == module_id)
        .first()
    )
    if not file:
        raise HTTPException(status_code=404, detail="File not found in this module")
    return file.content


def create_file(file: File, session: Session) -> File:
    session.add(file)
    session.commit()
    session.refresh(file)
    return file


def create_folder(folder: Folder, data: Dict[str, Any], session: Session) -> Folder:
    session.add(folder)
    session.commit()
    session.refresh(folder)
    if not isinstance(data, dict):
        data = data.dict()
    for filename, contents in data.items():
        if isinstance(contents, dict):
            contents = json.dumps(contents)

        file = File(name=filename, content=contents, folder_id=folder.id)
        create_file(file, session)
    return folder


def create_module_with_folders(
    module: ModuleSimple, folders: List[Tuple[str, Dict[str, Any]]], session: Session
) -> Module:
    session.add(module)
    session.commit()
    session.refresh(module)
    for title, files_content in folders:
        folder = Folder(name=title, module_id=module.id)
        create_folder(folder, files_content, session)
    return module


# Not Currently Active These are not yet implemented
def create_module(module: Module, session: Session) -> Module:
    session.add(module)
    session.commit()
    session.refresh(module)
    return module


def get_modules(
    skip: int = 0, limit: int = 10, session: Session = None
) -> List[Module]:
    return session.exec(select(Module).offset(skip).limit(limit)).all()
