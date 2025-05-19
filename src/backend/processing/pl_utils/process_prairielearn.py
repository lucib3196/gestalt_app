from typing import Dict, List
from bs4 import BeautifulSoup
from .TagReplacer import TagReplacer
from .tag_replacer_config import tag_replacer_configs
from .create_tag_replacer import create_tag_replacer


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
            mapping=cfg.get("mapping", {}),
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


def process(html: str):
    replacers = create_tag_replacer(html, tag_replacer_configs)
    modified_html = apply_tag_replacers(html, replacers)
    return modified_html


def main():
    """
    Main testing function. Runs HTML transformation using defined tag replacer configs.
    """
    html_examples = [
        {
            "description": "Example 1: Question panel with figure and checkbox",
            "html": r"""
                <pl-question-panel>
                  <pl-figure file-name="gas_laws.png"></pl-figure>
                  <p>The figure above illustrates concepts related to gases under certain conditions.</p>
                </pl-question-panel>
                <pl-checkbox answers-name="idealGas" weight="1" inline="true">
                  <pl-answer correct="true">\( PV = nRT \)</pl-answer>
                  <pl-answer correct="false">\( P = \rho RT \)</pl-answer>
                </pl-checkbox>
            """,
        },
        {
            "description": "Example 2: Multiple choice question block",
            "html": r"""
                <pl-multiple-choice answers-name="unitSystem" inline="true">
                  <pl-answer correct="true">SI Units</pl-answer>
                  <pl-answer correct="false">Imperial</pl-answer>
                </pl-multiple-choice>
            """,
        },
        {
            "description": "Example 3: Input panel with number input",
            "html": r"""
                <pl-input-panel>
                  <pl-number-input answers-name="forceValue" label="Enter the force:"></pl-number-input>
                </pl-input-panel>
            """,
        },
        {
            "description": "Example 4: Question panel with parameters and number input",
            "html": r"""
                <pl-question-panel>
                <p>
                A {{params.m}} {{params.unitsMass}} block of iron at temperature {{params.Ti}} {{params.unitsTemperature}} is supplied heat of {{params.Q}} {{params.unitsHeat}} so that the final temperature is {{params.Tf}} {{params.unitsTemperature}}.
                </p>
                </pl-question-panel>

                <p> Determine its final temperature. </p>
                <pl-number-input answers-name="Tf" comparison="sigfig" digits="3" label="Tf  (in {{params.unitsTemperature}})"></pl-number-input>
            """,
        },
        {
            "description": "Example 5: Pendulum problem with SVG and number inputs",
            "html": r"""
                <pl-question-panel>
                The 5 kg pendulum bob is released from rest when \( \theta = 0 \). Determine the initial tension in the cord. Also
                determine the tension at the instant \( \theta = 45^\circ \). Neglect the size of the bob and assume \( r = 2
                \mathrm{m} \).
                <p>
                    What are the initial tension (in {{params.unitsForce}}) and the tension at \( \theta = 45^\circ \) (in
                    {{params.unitsForce}})?
                </p>
                </pl-question-panel>

                {{params.svgString}}

                <pl-number-input answers-name="initial_tension" comparison="sigfig" digits="3"
                    label="Initial Tension"></pl-number-input>
                <pl-number-input answers-name="tension_theta_45" comparison="sigfig" digits="3"
                    label="Tension at \( \theta = 45^\circ \)"></pl-number-input>
            """,
        },
        {
            "description": "Example 5: Pendulum problem with SVG and number inputs",
            "html": """<pl-question-panel>
                <pl-figure file-name="reversedBraytonCycleSchematic.png"></pl-figure>

                <p>In the air refrigeration cycle illustrated, the main components include a compressor, a heat exchanger, and an expansion device. Energy is transferred as heat and work through the processes occurring between these components.</p>
                <ol>
                    <li><strong>Compressor</strong>: Increases the pressure and temperature of the refrigerant by performing work on it.</li>
                    <li><strong>Heat Exchanger</strong>: Transfers heat from the refrigerant to the external environment during its refrigeration cycle.</li>
                    <li><strong>Expansion Device</strong>: Reduces the pressure of the refrigerant, causing it to expand and cool. This process absorbs heat from the surroundings.</li>
                </ol>
                <p>Through this cycle, work is done on the refrigerant in the compressor, while heat is absorbed during the expansion process.</p>
            </pl-question-panel>
            <pl-multiple-choice answers-name="energyFlowInCycle" weight="1" inline="true">
                <pl-answer correct="true"> The compressor adds work to the system, while heat is removed at the heat exchanger, and heat is absorbed in the expansion phase.</pl-answer>
                <pl-answer correct="false"> Only heat is added to the refrigerant throughout the cycle.</pl-answer>
                <pl-answer correct="false"> The system only performs mechanical work without any heat exchanges.</pl-answer>
                <pl-answer correct="false"> The heat exchanger solely increases the refrigerant’s pressure.</pl-answer>
            </pl-multiple-choice>
            """,
        },
    ]

    print("PrairieLearn Tag Replacer Test Utility\n")
    for i, example in enumerate(html_examples, start=1):
        print(f"{'='*10} Test Case {i}: {example['description']} {'='*10}")
        html_string = example["html"]
        replacers = create_tag_replacer(html_string, tag_replacer_configs)
        modified_html = apply_tag_replacers(html_string, replacers)
        print("Input HTML:\n", html_string.strip())
        print("\nTransformed HTML:\n", modified_html)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
