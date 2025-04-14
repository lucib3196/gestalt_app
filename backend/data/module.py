# module.py (main entry point for local testing)
from contextlib import contextmanager
from .database import get_session
from .crud import get_all_folders
import asyncio

@contextmanager
def sync_session():
    gen = get_session()
    session = next(gen)
    try:
        yield session
    finally:
        gen.close()

if __name__ == "__main__":
    with sync_session() as session:
        print(get_all_folders(session=session))
