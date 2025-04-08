from typing import Dict, List
from bs4 import BeautifulSoup
from .TagReplacer import TagReplacer
from .tag_replacer_config import tag_replacer_configs


def create_tag_replacer(html_string: str, config: Dict[str, Dict]) -> List[TagReplacer]:
    """
    Create a list of TagReplacer instances from a given configuration.

    Args:
        html_string (str): The raw HTML string to parse.
        config (Dict[str, Dict]): A dictionary of tag replacement configurations.

    Returns:
        List[TagReplacer]: A list of initialized TagReplacer objects.
    """
    replacers = []
    for name, cfg in config.items():
        replacer = TagReplacer(
            html=html_string,
            target_tag=cfg.get("target_tag", ""),
            replacement_tag=cfg.get("replacement_tag", ""),
            attributes=cfg.get("attributes", {}),
            mapping=cfg.get("mapping", {})
        )
        replacers.append(replacer)
    return replacers


def apply_tag_replacers(html_string: str, replacers: List[TagReplacer]) -> str:
    """
    Apply a list of TagReplacer instances to a given HTML string.

    Args:
        html_string (str): The HTML to transform.
        replacers (List[TagReplacer]): A list of TagReplacer objects.

    Returns:
        str: The transformed HTML string.
    """
    soup = BeautifulSoup(html_string, "html.parser")

    for replacer in replacers:
        # print(f"[Before Replacement: <{replacer.target_tag}>]\n{soup}\n")
        replacer.update_soup(str(soup))
        soup = replacer.run()
        # print(f"[After Replacement: <{replacer.target_tag}>]\n{soup}\n")

    return soup.prettify()

def process(html:str):
    replacers = create_tag_replacer(html, tag_replacer_configs)
    modified_html = apply_tag_replacers(html, replacers)
    return modified_html


def main():
    """
    Main testing function. Runs HTML transformation using defined tag replacer configs.
    """
    html_examples = [
        # Example 1: Question panel with figure and checkbox
        r"""
        <pl-question-panel>
          <pl-figure file-name="gas_laws.png"></pl-figure>
          <p>The figure above illustrates concepts related to gases under certain conditions.</p>
        </pl-question-panel>
        <pl-checkbox answers-name="idealGas" weight="1" inline="true">
          <pl-answer correct="true">\( PV = nRT \)</pl-answer>
          <pl-answer correct="false">\( P = \rho RT \)</pl-answer>
        </pl-checkbox>
        """,

        # Example 2: Multiple choice question block
        r"""
        <pl-multiple-choice answers-name="unitSystem" inline="true">
          <pl-answer correct="true">SI Units</pl-answer>
          <pl-answer correct="false">Imperial</pl-answer>
        </pl-multiple-choice>
        """,

        # Example 3: Input panel with number input
        r"""
        <pl-input-panel>
          <pl-number-input answers-name="forceValue" label="Enter the force:"></pl-number-input>
        </pl-input-panel>
        """
    ]

    for i, html_string in enumerate(html_examples, start=1):
        print(f"\n{'='*20} Test Case {i} {'='*20}")
        replacers = create_tag_replacer(html_string, tag_replacer_configs)
        modified_html = apply_tag_replacers(html_string, replacers)
        print(f"Final Output (Test Case {i}):\n{modified_html}\n")


if __name__ == "__main__":
    main()
