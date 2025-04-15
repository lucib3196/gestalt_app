"""
CRUD and Download Services for Question Module Data

This module handles operations related to Packages, Question Folders, and Question Files.
It provides functions for retrieving data, creating new records, and downloading folders as ZIP files.
"""

# ─────────────────────────────────────────────────────────────
# Standard Library Imports
# ─────────────────────────────────────────────────────────────
import os
import json
import tempfile
import zipfile
from io import BytesIO
from typing import List, Tuple, Dict, Any, Optional

# ─────────────────────────────────────────────────────────────
# Third-Party Imports
# ─────────────────────────────────────────────────────────────
from fastapi import HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from sqlmodel import Session, select

# ─────────────────────────────────────────────────────────────
# Internal App Imports
# ─────────────────────────────────────────────────────────────
from .database import engine
from .helpers import create_zip_file
from ..model.question_models import Package, QuestionFolder, QuestionFile

# ─────────────────────────────────────────────────────────────
# CRUD Service Functions
# ─────────────────────────────────────────────────────────────

def get_package_folders(package_id: int, session: Session = None) -> List[QuestionFolder]:
    """
    Retrieve all question folders associated with a specific package.
    
    Args:
        package_id (int): The ID of the package.
        session (Session, optional): A SQLModel session. If not provided, the caller should supply one.
    
    Returns:
        List[QuestionFolder]: A list of question folders belonging to the package.
    
    Raises:
        HTTPException: If the package does not exist or no folders are found.
    """
    package = session.get(Package, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    folders = session.query(QuestionFolder).filter_by(package_id=package_id).all()
    if not folders:
        raise HTTPException(status_code=404, detail="Question folders not found")
    return folders

def get_folder_files(package_id: int, folder_id: int, session: Session = None) -> List[QuestionFile]:
    """
    Retrieve all question files within a specific folder of a package.

    Args:
        package_id (int): The package's ID.
        folder_id (int): The folder's ID.
        session (Session, optional): A SQLModel session.

    Returns:
        List[QuestionFile]: A list of question files associated with the folder.

    Raises:
        HTTPException: If the folder is not found.
    """
    get_package_folders(package_id=package_id, session=session)  # Ensures the package exists
    folder = session.query(QuestionFolder).filter_by(id=folder_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Question folder not found")
    return folder.question_files

def get_all_question_folders(skip: int = 0, limit: int = 10, session: Session = None) -> List[QuestionFolder]:
    """
    Retrieve all question folders with pagination.

    Args:
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to retrieve.
        session (Session, optional): A SQLModel session.

    Returns:
        List[QuestionFolder]: The list of retrieved question folders.
    """
    return session.exec(select(QuestionFolder).offset(skip).limit(limit)).all()

def get_package_by_id(package_id: int, session: Session = None) -> Package:
    """
    Retrieve a specific package by its ID.

    Args:
        package_id (int): The ID of the package.
        session (Session, optional): A SQLModel session.

    Returns:
        Package: The package matching the given ID.

    Raises:
        HTTPException: If the package is not found.
    """
    package = session.get(Package, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package

def get_package_folder(package_id: int, session: Session = None) -> QuestionFolder:
    """
    Retrieve the first question folder associated with a given package.

    Args:
        package_id (int): The package's ID.
        session (Session, optional): A SQLModel session.

    Returns:
        QuestionFolder: The first matching question folder.

    Raises:
        HTTPException: If no folder is found for the package.
    """
    folder = session.query(QuestionFolder).filter_by(package_id=package_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Question folder not found")
    return folder

def get_package_files(package_id: int, session: Session) -> List[QuestionFile]:
    """
    Retrieve all question files within the first folder of a package.

    Args:
        package_id (int): The package's ID.
        session (Session): A SQLModel session.

    Returns:
        List[QuestionFile]: The list of question files.

    Raises:
        HTTPException: If no folder is found for the package.
    """
    folder = session.query(QuestionFolder).filter_by(package_id=package_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Question folder not found")
    return folder.question_files

def get_packages(skip: int = 0, limit: int = 10, session: Session = None) -> List[Package]:
    """
    Retrieve a list of packages with pagination.

    Args:
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to retrieve.
        session (Session, optional): A SQLModel session.

    Returns:
        List[Package]: A list of packages.
    """
    return session.exec(select(Package).offset(skip).limit(limit)).all()

def get_single_file(package_id: int, file_id: int, session: Session) -> str:
    """
    Retrieve the content of a specific question file within a package.

    Args:
        package_id (int): The ID of the package.
        file_id (int): The ID of the file.
        session (Session): A SQLModel session.

    Returns:
        str: The file content.

    Raises:
        HTTPException: If the file is not found.
    """
    file = (
        session.query(QuestionFile)
        .join(QuestionFolder, QuestionFile.question_folder_id == QuestionFolder.id)
        .filter(QuestionFile.id == file_id, QuestionFolder.package_id == package_id)
        .first()
    )
    if not file:
        raise HTTPException(status_code=404, detail="Question file not found in this package")
    return file.content

def create_file(file: QuestionFile, session: Session) -> QuestionFile:
    """
    Create a new question file record.

    Args:
        file (QuestionFile): The question file to create.
        session (Session): A SQLModel session.

    Returns:
        QuestionFile: The created question file with an assigned ID.
    """
    session.add(file)
    session.commit()
    session.refresh(file)
    return file

def create_folder(folder: QuestionFolder, data: Dict[str, Any], session: Session) -> QuestionFolder:
    """
    Create a new question folder and its associated question files.

    Args:
        folder (QuestionFolder): The folder to create.
        data (Dict[str, Any]): A dictionary mapping file names to file contents.
        session (Session): A SQLModel session.

    Returns:
        QuestionFolder: The created question folder.
    """
    session.add(folder)
    session.commit()
    session.refresh(folder)
    if not isinstance(data, dict):
        data = data.dict()
    for filename, contents in data.items():
        if isinstance(contents, dict):
            contents = json.dumps(contents)
        file = QuestionFile(name=filename, content=contents, save_name=filename, question_folder_id=folder.id)
        create_file(file, session)
    return folder

def create_package_with_folders(
    package: Package,
    folders: List[Tuple[str, Dict[str, Any]]],
    session: Session
) -> Package:
    """
    Create a new package along with its associated question folders and files.

    Args:
        package (Package): The package to create.
        folders (List[Tuple[str, Dict[str, Any]]]): A list of tuples where each tuple contains
            the folder title and a dictionary of file data.
        session (Session): A SQLModel session.

    Returns:
        Package: The created package.
    """
    session.add(package)
    session.commit()
    session.refresh(package)
    for title, files_content in folders:
        folder = QuestionFolder(title=title, package_id=package.id)
        create_folder(folder, files_content, session)
    return package

def create_package(package: Package, session: Session) -> Package:
    """
    Create a new package record.

    Args:
        package (Package): The package to create.
        session (Session): A SQLModel session.

    Returns:
        Package: The created package.
    """
    session.add(package)
    session.commit()
    session.refresh(package)
    return package

# ─────────────────────────────────────────────────────────────
# Download Services
# ─────────────────────────────────────────────────────────────

# Mapping of file names to defaults for downloads.
file_name_map: Dict[str, str] = {
    "question_txt": "question.txt",
    "question_html": "question.html",
    "server_js": "server.js",
    "server_py": "server.py",
    "solution_html": "solution.html",
    "metadata": "info.json",
}

def download_single_folder(package_id: int, folder_id: int, session: Session):
    """
    Download a specific question folder as a ZIP file.
    
    This function retrieves a folder by its package ID and folder ID, writes its files
    to temporary files, and zips them up for download.

    Args:
        package_id (int): The package ID.
        folder_id (int): The folder ID.
        session (Session): A SQLModel session.

    Returns:
        StreamingResponse: A streaming response containing the ZIP file.
    
    Raises:
        HTTPException: If the folder is not found.
    """
    folder: QuestionFolder = (
        session.query(QuestionFolder)
        .filter(QuestionFolder.package_id == package_id, QuestionFolder.id == folder_id)
        .first()
    )
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found for this module")
    
    folder_name = folder.title
    folder_files: List[QuestionFile] = folder.question_files
    temp_filepaths = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for file in folder_files:
            tempfile_path = os.path.join(
                tmpdir,
                file.save_name if file.save_name is not None else file_name_map.get(file.name)
            )
            content = file.content
            if isinstance(content, str):
                content = content.encode("utf-8")
            elif isinstance(content, dict):
                content = json.dumps(content).encode("utf-8")
            with open(tempfile_path, "wb") as f:
                f.write(content)
            temp_filepaths.append(tempfile_path)
        zip_stream = create_zip_file(temp_filepaths)
        headers = {"Content-Disposition": f"attachment; filename={folder_name}.zip"}
        return StreamingResponse(zip_stream, media_type="application/zip", headers=headers)

def download_all_folders_in_module(package_id: int, session: Session):
    """
    Download a ZIP file containing all question folders for a given package.
    
    Each folder is zipped individually and then combined into a master ZIP file.

    Args:
        package_id (int): The package ID.
        session (Session): A SQLModel session.

    Returns:
        StreamingResponse: A streaming response containing the master ZIP file.
    
    Raises:
        HTTPException: If no folders are found for the package.
    """
    folders: List[QuestionFolder] = (
        session.query(QuestionFolder).filter(QuestionFolder.package_id == package_id).all()
    )

    if not folders:
        raise HTTPException(status_code=404, detail="No folders found for this module.")

    master_zip_buffer = BytesIO()

    with zipfile.ZipFile(master_zip_buffer, "w", zipfile.ZIP_DEFLATED) as master_zip:
        for folder in folders:
            folder_name = folder.title
            folder_id = folder.id
            folder_files: List[QuestionFile] = folder.question_files

            folder_zip_buffer = BytesIO()

            with zipfile.ZipFile(folder_zip_buffer, "w", zipfile.ZIP_DEFLATED) as folder_zip:
                for file in folder_files:
                    filename = file.save_name or file_name_map.get(file.name, file.name)
                    content = file.content
                    if isinstance(content, str):
                        content = content.encode("utf-8")
                    elif isinstance(content, dict):
                        content = json.dumps(content).encode("utf-8")
                    folder_zip.writestr(filename, content)

            folder_zip_buffer.seek(0)
            master_zip.writestr(f"{folder_name}_{folder_id}.zip", folder_zip_buffer.read())

    master_zip_buffer.seek(0)
    headers = {"Content-Disposition": f"attachment; filename=module_{package_id}_folders.zip"}

    return StreamingResponse(master_zip_buffer, media_type="application/zip", headers=headers)
