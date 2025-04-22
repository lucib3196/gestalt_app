from .create_tag_replacer import create_tag_replacer
from .tag_replacer_config import tag_replacer_configs

def main():
    html = r""""<pl-question-panel>
<p>
A {{params.m}} {{params.unitsMass}} block of iron at temperature {{params.Ti}} {{params.unitsTemperature}} is supplied heat of {{params.Q}} {{params.unitsHeat}} so that the final temperature is {{params.Tf}} {{params.unitsTemperature}}.
</p>
</pl-question-panel>

<p> Determine its final temperature. </p>
<pl-number-input answers-name="Tf" comparison="sigfig" digits="3" label="Tf  (in {{params.unitsTemperature}})"></pl-number-input>"""

    replacers = create_tag_replacer(html_string=html, config=tag_replacer_configs)
    print(replacers)


if __name__ == "__main__":
    main()