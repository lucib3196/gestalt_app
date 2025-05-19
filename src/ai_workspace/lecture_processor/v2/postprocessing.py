import json
import os
from .lecture_processing_v2 import LectureOutputState
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Union
import pandas as pd
from ...utils.plotting import gestalt_token_extraction, lecture_summary


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_path, "processed_lecture.json")

    # Load JSON data
    with open(filepath, "r") as f:
        raw_data = json.load(f)

    # Decode into Pydantic model
    parsed_data = LectureOutputState.model_validate(raw_data)

    # Get the generated lecture section
    generated = parsed_data.generated_lecture

    if not generated:
        print("No generated lecture found.")
        return

    # Write main final lecture
    if generated.final_lecture:
        with open(
            os.path.join(base_path, "final_lecture.md"), "w", encoding="utf-8"
        ) as f:
            f.write(generated.final_lecture)

    # Write derivations
    if generated.derivation_str:
        with open(
            os.path.join(base_path, "derivations.md"), "w", encoding="utf-8"
        ) as f:
            f.write(generated.derivation_str)

    # ⚠️ Only write lecture_base if it exists (but it's not in your current model)
    if hasattr(generated, "lecture_base") and generated.lecture_base:
        with open(
            os.path.join(base_path, "lecture_base.md"), "w", encoding="utf-8"
        ) as f:
            f.write(generated.lecture_base)

    # Write questions
    if generated.question_str:
        with open(os.path.join(base_path, "question.md"), "w", encoding="utf-8") as f:
            f.write(generated.question_str)

    summary = lecture_summary(parsed_data, show_plot=True)


if __name__ == "__main__":
    main()
