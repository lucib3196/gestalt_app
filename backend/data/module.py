# module.py (main entry point for local testing)
from contextlib import contextmanager
from data.database import get_session
from data.generate_quiz import generate_quiz

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
        generate_quiz(1, session)
