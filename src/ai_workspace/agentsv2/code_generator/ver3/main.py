from .code_generator import compiled_graph as code_generator_v3
from .code_generator import CodeGenInput, CodeGenState
from schemas import Question
import asyncio
from ai_workspace.utils import to_serializable


async def process_question(question: str):
    q_input = CodeGenInput(
        question_payload=Question(question=question), initial_metadata=None  # type: ignore
    )
    result = await code_generator_v3.ainvoke(q_input)
    return result


async def main(q_list: list[str]):
    tasks = [process_question(q) for q in q_list]
    results = await asyncio.gather(*tasks)
    return results


import os


def save_file(filename, content):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    q_list = [
        "A simply supported steel beam with a span of 4 meters carries a point load of 10 kN at its center. If the beam has a rectangular cross-section of width 100 mm and height 200 mm, what is the maximum bending stress in the beam? (Give your answer in MPa.)",
        # "A heat engine receives 5000 J of heat from a high-temperature reservoir and does 1200 J of work. What is the efficiency of the thermodynamic cycle? (Express your answer as a percentage.)",
    ]
    results = asyncio.run(main(q_list))

    path_to_save = r"./generate_question/"
    for idx, res in enumerate(results, 1):
        print(f"Result {idx}: {res}\nType: {type(res)}")
        data = CodeGenState(**res)
        qtitle = data.question_metadata.title or f"question_{idx}"
        # Sanitize qtitle for filesystem
        safe_qtitle = "".join(
            c for c in qtitle if c.isalnum() or c in (" ", "_", "-")
        ).rstrip()
        question_dir = os.path.join(path_to_save, safe_qtitle)
        os.makedirs(question_dir, exist_ok=True)

        files_to_save = {
            "question.html": data.files.question_html,
            "solution.html": data.files.solution_html,
            "server.js": data.files.server_js,
            "server.py": data.files.server_py,
        }

        for fname, content in files_to_save.items():
            if content:
                save_file(os.path.join(question_dir, fname), content)
