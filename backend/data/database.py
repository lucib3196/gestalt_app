# data/database.py
import os
from typing import Generator
from sqlmodel import SQLModel, Session, create_engine

# Set up the database file path.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)

# Create all tables at startup.
SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Yield a SQLModel session."""
    with Session(engine) as session:
        yield session
