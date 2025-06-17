import pandas as pd
from backend.model import QuestionFolder, File
from contextlib import contextmanager
from backend.data.database import get_session
from backend.data.question_models import *

filepath = r"data/QuestionDataV2_06122025_classified.csv"
df = pd.read_csv(filepath)

# Preprocess columns
df["prereqs"] = (
    df["prereqs"]
    .fillna("")
    .apply(lambda x: [s.strip() for s in x.split(",") if s.strip()])
)
df["tags"] = (
    df["tags"]
    .fillna("")
    .apply(lambda x: [s.strip() for s in x.split(",") if s.strip()])
)
df["topics"] = (
    df["topic"]
    .fillna("")
    .apply(lambda x: [s.strip() for s in x.split(",") if s.strip()])
)
df["relevant_courses"] = (
    df["relevant_courses"]
    .fillna("")
    .apply(lambda x: [s.strip() for s in x.split(",") if s.strip()])
)

file_mapping = [
    ("question.html", "question.html"),
    ("server.js", "server.js"),
    ("server.py", "server.py"),
    ("solution.html", "solution.html"),
    ("properties.js", "properties.js"),
    ("info.json", "info.json"),
]

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
        for idx, row in df.iterrows():
            title = row["Question Title"]
            topic = row["topics"]
            tags = row["tags"]
            prereqs = row["prereqs"]
            relevant_course = row["relevant_courses"]
            isadaptive = row["isAdaptive"]
            ai_generated = False
            created_by = row["createdBy"]
            reviewers = []
            reviewed = False

            files_data = {}
            for fname, cname in file_mapping:
                content = row.get(cname, None)
                if pd.notna(content) and str(content).strip():
                    files_data[fname] = content

            question = QuestionFolder(
                title=title,
                topic=topic,
                tags=tags,
                pre_reqs=prereqs,
                relevant_courses=relevant_course,
                is_adaptive=isadaptive,
                ai_generated=ai_generated,
                created_by=created_by,
                reviewers=reviewers,
                reviewed=reviewed,
            )

            create_question_folder(question, data=files_data, session=session)
