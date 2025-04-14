from typing import List, Tuple, Dict, Any, Optional
from sqlmodel import Session, select
from fastapi import HTTPException
from .database import engine
from ..model.question_models import Package, QuestionFolder, QuestionFile
import json

# Retrieve all question folders associated with a specific package
def get_package_folders(package_id: int, session: Session = None) -> List[QuestionFolder]:
    package = session.get(Package, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    folders = session.query(QuestionFolder).filter_by(package_id=package_id).all()
    if not folders:
        raise HTTPException(status_code=404, detail="Question folders not found")
    return folders

# Retrieve all question files within a specific question folder of a package
def get_folder_files(package_id: int, folder_id: int, session: Session = None) -> List[QuestionFile]:
    get_package_folders(package_id=package_id, session=session)  # Ensures the package exists
    folder = session.query(QuestionFolder).filter_by(id=folder_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Question folder not found")
    return folder.question_files

# Retrieve a specific package by ID
def get_package_by_id(package_id: int, session: Session = None) -> Package:
    package = session.get(Package, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package

# Retrieve a specific question folder within a package
def get_package_folder(package_id: int, session: Session = None) -> QuestionFolder:
    folder = session.query(QuestionFolder).filter_by(package_id=package_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Question folder not found")
    return folder

# Retrieve all question files within the first question folder of a package
def get_package_files(package_id: int, session: Session) -> List[QuestionFile]:
    folder = session.query(QuestionFolder).filter_by(package_id=package_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Question folder not found")
    return folder.question_files

# Retrieve a list of packages with pagination
def get_packages(skip: int = 0, limit: int = 10, session: Session = None) -> List[Package]:
    return session.exec(select(Package).offset(skip).limit(limit)).all()

# Retrieve the content of a specific question file within a package
def get_single_file(package_id: int, file_id: int, session: Session) -> str:
    file = (
        session.query(QuestionFile)
        .join(QuestionFolder, QuestionFile.question_folder_id == QuestionFolder.id)
        .filter(QuestionFile.id == file_id, QuestionFolder.package_id == package_id)
        .first()
    )
    if not file:
        raise HTTPException(status_code=404, detail="Question file not found in this package")
    return file.content

# Create a new question file
def create_file(file: QuestionFile, session: Session) -> QuestionFile:
    session.add(file)
    session.commit()
    session.refresh(file)
    return file

# Create a new question folder and its associated question files
def create_folder(folder: QuestionFolder, data: Dict[str, Any], session: Session) -> QuestionFolder:
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

# Create a new package along with its associated question folders and files
def create_package_with_folders(
    package: Package,
    folders: List[Tuple[str, Dict[str, Any]]],
    session: Session
) -> Package:
    session.add(package)
    session.commit()
    session.refresh(package)
    for title, files_content in folders:
        folder = QuestionFolder(title=title, package_id=package.id)
        create_folder(folder, files_content, session)
    return package

# Create a new package
def create_package(package: Package, session: Session) -> Package:
    session.add(package)
    session.commit()
    session.refresh(package)
    return package
