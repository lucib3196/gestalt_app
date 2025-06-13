import pandas as pd
import asyncio
from src.ai_workspace.agentsv2.question_topic_classification_agent.question_topic_classification_agent import (
    app as classification_graph,
)


input_path = r"src\data\QuestionDataV2_06122025_classified.csv"
output_path = r"src\data\QuestionDataV2_06122025_classified.csv"
df = pd.read_csv(input_path)
mask = (~df["question"].isna()) & (~df["isAdaptive"].isna())
filtered_df = df[mask].copy()
filtered_df = filtered_df[mask].copy()
questions = filtered_df["question"].tolist()
# print(filtered_df.columns)

for i, q in enumerate(questions):
    try:
        results = classification_graph.invoke({"question": q})
        topics = results.get("topic_classification_result", None)
        if topics:
            value = (
                ", ".join(topics.topics)
                if isinstance(topics.topics, list)
                else str(topics.topics)
            )
        else:
            value = None
        filtered_df.at[filtered_df.index[i], "topics"] = value
    except Exception as e:
        print(f"Error processing question at index {i}: {e}")
        filtered_df.at[filtered_df.index[i], "topics"] = None
print(filtered_df)
filtered_df.to_csv(output_path, index=False)
