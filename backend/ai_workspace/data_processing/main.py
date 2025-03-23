import os 
import sqlite3
import pandas as pd


current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, '..', 'data', 'Question_Embedding_20241230.csv')
db_path = os.path.join(current_dir, '..','data', 'question_embedding_db.db')

df = pd.read_csv(file_path,encoding="utf-8", dtype=str)
df = df.astype(str)
print(df["question.html"])

conn = sqlite3.connect(db_path)

df.to_sql("question_data", conn, if_exists="replace", index=False)
conn.close()