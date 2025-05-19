import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ..lecture_processor.v2.lecture_processing_v2 import LectureOutputState
from typing import Optional

def gestalt_token_extraction(
    data: LectureOutputState, show_plot: bool = False, save_path: str = None
):
    """
    Extracts and visualizes token usage from Gestalt modules in a lecture.

    Args:
        data (LectureOutputState): The lecture output containing Gestalt modules.
        show_plot (bool): Whether to display the plot (useful for headless scripts).

    Returns:
        dict: Contains the plot (fig, ax) and two DataFrames:
            - sum_df: Aggregated token counts by step.
            - describe_df: Descriptive stats per step.
    """
    gestalt_modules = data.gestalt_modules

    # Ensure Gestalt Modules has something
    if not gestalt_modules:
        return None

    # Extract the tokens per module
    rows = []
    for module in gestalt_modules:
        for step in module.token_usage:
            rows.append(
                {
                    "question_title": module.question_metadata.title,
                    "step_name": step.step_name,
                    "prompt_tokens": step.token_usage.prompt_tokens,
                    "completion_tokens": step.token_usage.completion_tokens,
                    "total_tokens": step.token_usage.total_tokens,
                }
            )
    # Contains the main data as a dataframe
    main_df = pd.DataFrame(rows)

    # Aggregate of per step name
    df_group = main_df.groupby("step_name")[
        ["prompt_tokens", "completion_tokens", "total_tokens"]
    ]
    df_sum = df_group.sum()
    full_analysis = df_group.describe()

    # Create bar chart for overall summary
    # Extract values
    step_names = df_sum.index.tolist()
    prompt = df_sum["prompt_tokens"].to_numpy()
    completion = df_sum["completion_tokens"].to_numpy()

    x = np.arange(len(step_names))
    width = 0.6

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x, prompt, width, label="Prompt Tokens")
    ax.bar(x, completion, width, bottom=prompt, label="Completion Tokens")

    ax.set_xticks(x)
    ax.set_xticklabels(step_names, rotation=45, ha="right")
    ax.set_ylabel("Token Count")
    ax.set_title("Token Usage Summary per Lecture – \n Gestalt Module Breakdown")
    ax.legend(loc="upper right")
    ax.grid(True, axis="y", linestyle="--", alpha=0.5)

    # Get the full token summary
    total_tokens = df_sum["total_tokens"].sum()
    ax.text(
        0,
        1,
        f"Total Tokens:\n{total_tokens:,}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#f0f0f0", edgecolor="gray"),
    )

    # Showing and saving plots
    if show_plot:
        plt.tight_layout()
        plt.show()
    else:
        plt.close(fig)

    if save_path:
        fig.savefig(save_path)

    return {
        "plot": (fig, ax),
        "dataframes": {"summary": df_sum, "description": full_analysis, "raw": main_df},
    }


def lecture_summary(
    data: LectureOutputState,
    show_plot: bool = False,
    save_path: Optional[str] = None,
):
    """
    Generates a summary of token usage for a lecture, including both
    top-level processing steps and the Gestalt module generator steps.

    Args:
        data (LectureOutputState): The full lecture output object containing token usage.
        show_plot (bool, optional): If True, displays the token usage bar chart. Defaults to False.
        save_path (str, optional): If provided, saves the chart to this file path.

    Returns:
        dict: Contains the following keys:
            - "plot": (fig, ax) tuple of the matplotlib figure and axis
            - "dataframe": The grouped token summary DataFrame
            - "raw_data": The raw token DataFrame for all steps
            - "total_tokens": Sum of all tokens used
    """

    # Collect top-level step token usage
    rows = [
        {
            "step_name": usage.step_name,
            "prompt_tokens": usage.token_usage.prompt_tokens,
            "completion_tokens": usage.token_usage.completion_tokens,
            "total_tokens": usage.token_usage.total_tokens,
        }
        for usage in data.total_token_usage
    ]

    # Include Gestalt module token breakdown if present
    gestalt_data = gestalt_token_extraction(data, show_plot)
    if gestalt_data:
        df_gestalt = gestalt_data["dataframes"]["summary"]
        rows.append(
            {
                "step_name": "Gestalt Module Generator",
                "prompt_tokens": df_gestalt["prompt_tokens"].sum(),
                "completion_tokens": df_gestalt["completion_tokens"].sum(),
                "total_tokens": df_gestalt["total_tokens"].sum(),
            }
        )

    # Create main DataFrame and group by step
    main_df = pd.DataFrame(rows)
    df_group = main_df.groupby("step_name")[
        ["prompt_tokens", "completion_tokens", "total_tokens"]
    ]
    df_sum = df_group.sum().sort_values(by="total_tokens", ascending=False)

    # Plotting setup
    step_names = df_sum.index.tolist()
    prompt = df_sum["prompt_tokens"].to_numpy()
    completion = df_sum["completion_tokens"].to_numpy()
    x = np.arange(len(step_names))
    width = 0.6

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x, prompt, width, label="Prompt Tokens")
    ax.bar(x, completion, width, bottom=prompt, label="Completion Tokens")

    ax.set_xticks(x)
    ax.set_xticklabels(step_names, rotation=45, ha="right")
    ax.set_ylabel("Token Count")
    ax.set_title("Token Usage Summary per Lecture")
    ax.legend(loc="upper right")
    ax.grid(True, axis="y", linestyle="--", alpha=0.5)

    # Add total token annotation
    total_tokens = df_sum["total_tokens"].sum()
    ax.text(
        0,
        1,
        f"Total Tokens:\n{total_tokens:,}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#f0f0f0", edgecolor="gray"),
    )

    # Show or save plot
    if show_plot:
        plt.tight_layout()
        plt.show()
    else:
        plt.close(fig)

    if save_path:
        fig.savefig(save_path)

    return {
        "lecture_analysis": {
            "plot": (fig, ax),
            "dataframe": df_sum,
            "raw_data": main_df,
        },
        "gestalt_analysis": gestalt_data,
    }
