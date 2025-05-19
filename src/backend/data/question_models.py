# """
# CRUD and Download Services for Question Module Data

# This module handles operations related to Packages, Question Folders, and Question Files.
# It provides functions for retrieving data, creating new records, and downloading folders as ZIP files.
# """

# # ─────────────────────────────────────────────────────────────
# # Standard Library Imports
# # ─────────────────────────────────────────────────────────────
# import os
# import json
# import tempfile
# import zipfile
# from io import BytesIO
# from typing import List, Tuple, Dict, Any, Optional, Union

# # ─────────────────────────────────────────────────────────────
# # Third-Party Imports
# # ─────────────────────────────────────────────────────────────
# from fastapi import HTTPException
# from fastapi.responses import FileResponse, StreamingResponse
# from sqlmodel import Session, select

# # ─────────────────────────────────────────────────────────────
# # Internal App Imports
# # ─────────────────────────────────────────────────────────────
# from .database import engine
# from .helpers import create_zip_file
# from ..model.question_models import Package, QuestionFolder, File

# # ─────────────────────────────────────────────────────────────
# # CRUD Service Functions
# # ─────────────────────────────────────────────────────────────


# # ─────────────────────────────────────────────────────────────
# # Download Services
# # ─────────────────────────────────────────────────────────────


# def download_single_folder(package_id: int, folder_id: int, session: Session):
#     """
#     Download a specific question folder as a ZIP file.

#     This function retrieves a folder by its package ID and folder ID, writes its files
#     to temporary files, and zips them up for download.

#     Args:
#         package_id (int): The package ID.
#         folder_id (int): The folder ID.
#         session (Session): A SQLModel session.

#     Returns:
#         StreamingResponse: A streaming response containing the ZIP file.

#     Raises:
#         HTTPException: If the folder is not found.
#     """
#     folder: QuestionFolder = (
#         session.query(QuestionFolder)
#         .filter(QuestionFolder.package_id == package_id, QuestionFolder.id == folder_id)
#         .first()
#     )
#     if not folder:
#         raise HTTPException(status_code=404, detail="Folder not found for this module")

#     folder_name = folder.title
#     folder_files: List[QuestionFile] = folder.question_files
#     temp_filepaths = []
#     with tempfile.TemporaryDirectory() as tmpdir:
#         for file in folder_files:
#             tempfile_path = os.path.join(
#                 tmpdir,
#                 (
#                     file.save_name
#                     if file.save_name is not None
#                     else file_name_map.get(file.name)
#                 ),
#             )
#             content = file.content
#             if isinstance(content, str):
#                 content = content.encode("utf-8")
#             elif isinstance(content, dict):
#                 content = json.dumps(content).encode("utf-8")
#             with open(tempfile_path, "wb") as f:
#                 f.write(content)
#             temp_filepaths.append(tempfile_path)
#         zip_stream = create_zip_file(temp_filepaths)
#         headers = {"Content-Disposition": f"attachment; filename={folder_name}.zip"}
#         return StreamingResponse(
#             zip_stream, media_type="application/zip", headers=headers
#         )


# def download_all_folders_in_module(package_id: int, session: Session):
#     """
#     Download a ZIP file containing all question folders for a given package.

#     Each folder is zipped individually and then combined into a master ZIP file.

#     Args:
#         package_id (int): The package ID.
#         session (Session): A SQLModel session.

#     Returns:
#         StreamingResponse: A streaming response containing the master ZIP file.

#     Raises:
#         HTTPException: If no folders are found for the package.
#     """
#     folders: List[QuestionFolder] = (
#         session.query(QuestionFolder)
#         .filter(QuestionFolder.package_id == package_id)
#         .all()
#     )

#     if not folders:
#         raise HTTPException(status_code=404, detail="No folders found for this module.")

#     master_zip_buffer = BytesIO()

#     with zipfile.ZipFile(master_zip_buffer, "w", zipfile.ZIP_DEFLATED) as master_zip:
#         for folder in folders:
#             folder_name = folder.title
#             folder_id = folder.id
#             folder_files: List[QuestionFile] = folder.question_files

#             folder_zip_buffer = BytesIO()

#             with zipfile.ZipFile(
#                 folder_zip_buffer, "w", zipfile.ZIP_DEFLATED
#             ) as folder_zip:
#                 for file in folder_files:
#                     filename = file.save_name or file_name_map.get(file.name, file.name)
#                     content = file.content
#                     if isinstance(content, str):
#                         content = content.encode("utf-8")
#                     elif isinstance(content, dict):
#                         content = json.dumps(content).encode("utf-8")
#                     folder_zip.writestr(filename, content)

#             folder_zip_buffer.seek(0)
#             master_zip.writestr(
#                 f"{folder_name}_{folder_id}.zip", folder_zip_buffer.read()
#             )

#     master_zip_buffer.seek(0)
#     headers = {
#         "Content-Disposition": f"attachment; filename=module_{package_id}_folders.zip"
#     }

#     return StreamingResponse(
#         master_zip_buffer, media_type="application/zip", headers=headers
#     )


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
from typing import List, Tuple, Dict, Any, Optional, Union
from pydantic import BaseModel

# ─────────────────────────────────────────────────────────────
# Third-Party Imports
# ─────────────────────────────────────────────────────────────
from fastapi import HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from sqlmodel import Session, select
from ast import literal_eval

# ─────────────────────────────────────────────────────────────
# Internal App Imports
# ─────────────────────────────────────────────────────────────
from backend.model.question_models import QuestionFolder, File, Package, PackageContents
from backend.ai_workspace.code_generator.v2.code_generator import CodeGenState


# Mapping of file names to defaults for downloads.
file_name_map: Dict[str, str] = {
    "question_txt": "question.txt",
    "question_html": "question.html",
    "server_js": "server.js",
    "server_py": "server.py",
    "solution_html": "solution.html",
    "metadata": "info.json",
}


# Deleting Methods
def delete_package(package_id: int, session: Session = None):
    statement = select(Package).where(Package.id == package_id)
    results = session.exec(statement)
    package = results.one()

    session.delete(package)
    session.commit()

    if package is None:
        print(f"There is no package {package.name}")


# Basic Retrievers
def get_package(package_id: int, session: Session = None) -> Package:
    package = session.get(Package, package_id)
    # Checks
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    return package


def get_packages(
    skip: int = 0, limit: int = 10, session: Session = None
) -> List[Package]:
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


def get_question_folder(folder_id: int, session: Session = None) -> QuestionFolder:
    statement = select(QuestionFolder).where((QuestionFolder.id == folder_id))
    results = session.exec(statement)
    question_folder = results.first()
    if not question_folder:
        raise HTTPException(status_code=404, detail="Question folder not found")
    return question_folder


def get_package_questions(
    package_id: int, session: Session = None
) -> List[QuestionFolder]:
    package = session.get(Package, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    query = select(QuestionFolder).where((QuestionFolder.package_id == package_id))
    folders = session.exec(query).all()
    if not folders:
        raise HTTPException(status_code=404, detail="Question folders not found")
    return folders


def get_all_questions(skip: int, limit: int, session: Session = None):
    return session.exec(select(QuestionFolder).offset(skip).limit(limit)).all()


def get_question_files(folder_id: int, session: Session = None) -> List[File]:
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
    question = get_question_folder(folder_id=folder_id, session=session)
    return question.files


def get_question_file(folder_id: int, filename: str, session=None) -> File:
    statement = select(File).where(
        File.question_folder_id == folder_id,
        File.filename == filename,
    )
    file = session.exec(statement).first()
    if not file:
        return HTTPException(404, detail="File not found ")
    return file


def get_package_file(package_id: int, filename: str, session=None) -> File:
    statement = select(File).where(
        File.package_id == package_id,
        File.filename == filename,
    )
    file = session.exec(statement).first()
    if not file:
        return HTTPException(404, detail="File not found ")
    return file


def get_package_files(package_id: int, session=None) -> List[File]:
    statement = select(File).where(
        File.package_id == package_id,
    )
    files = session.exec(statement).all()
    if not files:
        return HTTPException(404, detail="Files not found ")
    return files


def get_package_contents(package_id: int, session=None) -> PackageContents:
    # Try to get file
    try:
        package = get_package(package_id, session)
        if not package:
            return HTTPException(404, detail="Package not found ")

        # Retrieve the questions associated with the package
        query = select(QuestionFolder).where((QuestionFolder.package_id == package_id))
        questions = session.exec(query).all()

        statement = select(File).where(
            File.package_id == package_id,
        )
        files = session.exec(statement).all()

    except HTTPException:
        raise  # re-raise custom HTTP errors
    except Exception as e:
        print(f"Error retrieving package contents: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return PackageContents(
        package=package,
        questions=questions if questions else [],
        files=files if files else [],
    )


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


def create_file(file: File, session: Session) -> File:
    """
    Create a new question file record.

    Args:
        file (QuestionFile): The question file to create.
        session (Session): A SQLModel session.

    Returns:
        QuestionFile: The created question file with an assigned ID.
    """
    if isinstance(file.content, dict):
        file.content = json.dumps(file.content)
    session.add(file)
    session.commit()
    session.refresh(file)
    return file


def create_question_folder(
    question_folder: QuestionFolder, data: Dict[str, Any], session: Session
) -> QuestionFolder:
    """
    Create a new QuestionFolder and its associated File records.

    Args:
        question_folder: unsaved QuestionFolder instance
        data: mapping of filename -> content (or nested dict)
        session: active SQLModel session

    Returns:
        The persisted QuestionFolder with files attached.
    """
    # 1) Persist the folder
    session.add(question_folder)
    session.commit()
    session.refresh(question_folder)

    # 2) Ensure we have a plain dict
    if not isinstance(data, dict) and hasattr(data, "dict"):
        data = data.dict()

    print(f"This is the data ", data)

    # 3) Create each File
    for filename, contents in data.items():
        # If the “contents” itself is a dict or list, serialize it
        if isinstance(contents, (dict, list)):
            contents = json.dumps(contents)

        file_obj = File(
            filename=filename,
            content=contents,
            question_folder_id=question_folder.id,
        )
        create_file(file_obj, session)

    return question_folder


def create_question_pack_v2(
    package: Package, qpacks: List[CodeGenState], session: Session
) -> List[QuestionFolder]:
    created_folders: List[QuestionFolder] = []

    for raw_qpack in qpacks:
        # 1) Ensure we have a CodeGenState, whether it started life
        #    as a dict or already as an instance:
        if not isinstance(raw_qpack, CodeGenState):
            qpack = CodeGenState(**raw_qpack)
        else:
            qpack = raw_qpack

        # 2) Unpack metadata & files
        q_meta = qpack.question_metadata
        q_initial = qpack.initial_metadata
        q_files = qpack.files

        # 3) Flatten prereqs
        prereqs_obj = q_meta.prereqs or []
        flat_prereqs: List[str] = []
        if hasattr(prereqs_obj, "dict"):
            for v in prereqs_obj.dict().values():
                if isinstance(v, list):
                    flat_prereqs.extend(v)
                elif isinstance(v, str):
                    flat_prereqs.append(v)
        else:
            flat_prereqs = list(prereqs_obj)

        # 4) Bool flags / creator
        if q_initial:
            raw_flag = q_initial.ai_generated
            ai_gen_flag = (
                literal_eval(raw_flag) if isinstance(raw_flag, str) else raw_flag
            )
            creator = q_initial.createdBy
        else:
            ai_gen_flag = True
            creator = ""

        # 5) Build & save the QuestionFolder
        question_folder = QuestionFolder(
            title=q_meta.title,
            topic=q_meta.topic,
            tags=q_meta.tags,
            pre_reqs=flat_prereqs,
            is_adaptive=literal_eval(q_meta.isAdaptive),
            ai_generated=ai_gen_flag,
            reviewers=None,
            reviewed=False,
            created_by=creator,
            package_id=package.id,
        )
        saved_folder = create_question_folder(
            question_folder=question_folder,
            data=q_files,
            session=session,
        )
        created_folders.append(saved_folder)

    return created_folders


def update_filecontents(
    folder_id: int, file_name: str, new_content: str, session: Session
) -> File:

    if file_name == "metadata":
        print("Updating metadata")
        return update_metadata(
            folder_id=folder_id, updates=new_content, session=session
        )
    else:

        statement = select(File).where(
            (File.filename == file_name) & (File.question_folder_id == folder_id)
        )
        result = session.exec(statement)
        file = result.first()

        if not file:
            raise ValueError("File not found")

        print("This is the old content", print(file.content))
        file.content = new_content
        session.add(file)
        session.commit()
        session.refresh(file)

        return file


def update_metadata(folder_id: int, updates: Union[dict, str], session: Session):
    # Search through database
    statement = select(File).where(
        (File.name == "metadata") & (File.question_folder_id == folder_id)
    )
    result = session.exec(statement)
    file = result.first()

    statement = select(QuestionFolder).where(QuestionFolder.id == folder_id)
    result = session.exec(statement)
    folder = result.first()

    if not file:
        raise ValueError("File not found")
    if not folder:
        raise ValueError("Folder Not Found")

    try:
        # Retrieve the current file content
        content = json.loads(file.content)
        # Handle just incase updates is not a string
        if isinstance(updates, str):
            updates = json.loads(updates)
        # Override old values and add new values
        for key, value in updates.items():
            content[key] = value

        print(f"This is the new content ", content)
        file.content = json.dumps(content)

        #
        valid_updates = {
            key: value
            for key, value in updates.items()
            if key in QuestionFolder.model_fields
        }

        updated_folder = folder.model_copy(update=valid_updates)
        print(valid_updates)

        print("This is the updated folder", updated_folder)

        session.add(file)
        session.commit()
        session.refresh(file)

        session.add(updated_folder)
        session.commit()
        session.refresh(updated_folder)
        return file, updated_folder
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON provided in content.")
