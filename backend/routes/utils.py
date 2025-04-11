from typing import List, Tuple
from sqlmodel import Session
from fastapi import Depends

from ..data.module import get_session
from ..data import crud as service
from ..model.module_db import ModuleSimple


async def save_generated_module(
    folders: List[Tuple[str, dict[str, str]]],
    title: str = "Module",
    session: Session = Depends(get_session)
):
    """
    Saves generated folders and their files to the database under a new module.
    
    Args:
        folders: A list of tuples containing folder names and their file contents.
        title: The name of the module to create.
        session: The database session dependency.

    Returns:
        The created module instance.
    """
    module = ModuleSimple(name=title)
    return service.create_module_with_folders(module, folders=folders, session=session)
