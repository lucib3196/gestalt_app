from typing import Dict, Optional
from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString
from copy import copy


class TagReplacer:
    """
    A utility class to parse HTML and replace specific tags with new ones,
    optionally mapping and merging attributes during the replacement process.

    Example use:
        replacer = TagReplacer(
            html="<custom-tag attr='value'></custom-tag>",
            target_tag="custom-tag",
            replacement_tag="div",
            attributes={"class": "my-class"},
            mapping={"attr": "data-attr"}
        )
        updated_html = replacer.run()
    """

    def __init__(
        self,
        html: str,
        target_tag: str,
        replacement_tag: str,
        attributes: Optional[Dict[str, str]] = None,
        mapping: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize the TagReplacer.

        Args:
            html (str): The HTML content to modify.
            target_tag (str): The tag to search for and replace.
            replacement_tag (str): The tag name to replace the target tag with.
            attributes (dict, optional): Base attributes to apply to the new tag.
            mapping (dict, optional): Attribute mapping from old → new attribute names.
        """
        self.html = html
        self.target_tag = target_tag
        self.replacement_tag = replacement_tag
        self.attributes: Dict[str, str] = attributes or {}
        self.mapping: Dict[str, str] = mapping or {}
        # Clean the html for better parsing
        cleaned_html = self.html.replace('\\"', '"')
        self.soup: BeautifulSoup = BeautifulSoup(cleaned_html, "html.parser")

    def map_attributes(
        self, old_attrs: Dict[str, str], mapping: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Maps old attributes to new attribute names using a provided mapping.

        Args:
            old_attrs (Dict[str, str]): The original tag's attributes.
            mapping (Dict[str, str]): Mapping of old → new attribute names.

        Returns:
            Dict[str, str]: New attributes after mapping.
        """
        new_attrs = {
            new_key: old_attrs[old_key]
            for old_key, new_key in mapping.items()
            if old_key in old_attrs
        }

        unmapped_keys = set(old_attrs.keys()) - set(mapping.keys())
        if unmapped_keys:
            print(f"[Warning] Unmapped attributes: {unmapped_keys}")
        return new_attrs

    def replace_tag(self) -> BeautifulSoup:
        """
        Replace all instances of the target tag with the replacement tag.

        Returns:
            BeautifulSoup: Modified soup with tags replaced.
        """

        container = self.soup.new_tag(name="div")
        container["class"] = self.target_tag
        for tag in self.soup.find_all(self.target_tag):
            mapped_attrs = self.map_attributes(tag.attrs, self.mapping)
            merged_attrs = {**self.attributes, **mapped_attrs}

            new_tag = self.soup.new_tag(name=self.replacement_tag, attrs=merged_attrs)

            print(tag.contents)
            for child in tag.contents:
                if isinstance(child, NavigableString) and not child.strip():
                    continue  # skip whitespace
                new_tag.append(copy(child))

            tag.replace_with(new_tag)

            new_tag = self.handle_labels(
                new_tag, merged_attrs, className=f"form-label {tag.name}"
            )
            # print(f"This is the new tag {new_tag}")
            container.append(new_tag)
        self.soup.append(container)

        return self.soup

    def replace_tag_unique(self) -> BeautifulSoup:
        """
        Replace a single instance of the target tag.

        Returns:
            BeautifulSoup: Modified soup with the single tag replaced.
        """
        tag = self.soup.find(self.target_tag)
        if tag:
            mapped_attrs = self.map_attributes(tag.attrs, self.mapping)
            merged_attrs = {**self.attributes, **mapped_attrs}

            new_tag = self.soup.new_tag(
                name=self.replacement_tag,
                attrs=merged_attrs,
                className=f"form-label {tag.name}",
            )

            for child in list(tag.children):
                new_tag.append(child.extract())

            tag.replace_with(new_tag)

            self.handle_labels(new_tag, merged_attrs)

        return self.soup

    def handle_labels(
        self, new_tag: Tag, merged_attrs: dict[str, str], className: str = "form-label"
    ):
        """
        Wraps a new_tag with a <label> tag if a 'label' key exists in merged_attrs.

        Args:
            new_tag (Tag): The BeautifulSoup tag to wrap.
            merged_attrs (dict[str, str]): Attributes including optional 'label'.
            className (str): The class to apply to the <label> tag. Default is 'form-label'.

        Returns:
            BeautifulSoup: The updated soup object.
        """
        label = merged_attrs.get("label", "")
        if label:
            label_tag = self.soup.new_tag("label", attrs={"class": className})
            label_tag.string = label
            new_tag.wrap(label_tag)
            return label_tag
        return ""

    def run(self) -> BeautifulSoup:
        """
        Run the replacer logic based on number of matches found.

        Returns:
            BeautifulSoup: The final modified soup.
        """
        try:
            tags = self.soup.find_all(self.target_tag)
            if not tags:
                # print(f"[Info] No tags found for <{self.target_tag}>.")
                return self.soup
            elif len(tags) == 1:

                return self.replace_tag_unique()
            else:
                # print(f"Handling Multiple {tags}")
                return self.replace_tag()
        except Exception as e:
            # print(f"[Error] Could not process <{self.target_tag}>: {e}")
            return self.soup

    def update_soup(self, html: str) -> None:
        """
        Replace the current soup with a new HTML string.

        Args:
            html (str): The new HTML content.
        """
        self.soup = BeautifulSoup(html, "html.parser")


def main():
    html_string = r"""
    <pl-question-panel>
      <pl-figure file-name="gas_laws.png"></pl-figure>
      <p>The figure above illustrates concepts related to gases under certain conditions.
         Which of the following is the ideal gas law equation?
      </p>
    </pl-question-panel>


    <pl-checkbox answers-name="idealGas" weight="1" inline="true">
      <pl-answer correct="true">\( PV = nRT \)</pl-answer>
      <pl-answer correct="false">\( P = \rho RT \)</pl-answer>
      <pl-answer correct="false">\( P = \frac{m}{V} \)</pl-answer>
      <pl-answer correct="false">\( P = \frac{RT}{m} \)</pl-answer>
    </pl-checkbox>
    """

    html_string2 = r""""<pl-question-panel>
<p>
A {{params.m}} {{params.unitsMass}} block of iron at temperature {{params.Ti}} {{params.unitsTemperature}} is supplied heat of {{params.Q}} {{params.unitsHeat}} so that the final temperature is {{params.Tf}} {{params.unitsTemperature}}.
</p>
</pl-question-panel>

<p> Determine its final temperature. </p>
<pl-number-input answers-name="Tf" comparison="sigfig" digits="3" label="Tf  (in {{params.unitsTemperature}})"></pl-number-input>"""

    html_string3 = r"""<pl-solution-panel>\r\n    <pl-figure file-name=\"3dMoment1.png\"></pl-figure>\r\n    <pl-hint level=\"1\" data-type=\"text\">First, you must identify the force vector. The red vector in the picture is just there to show the location and direction of the force, but it is not the actual force vector. In order to obtain the force vector you must multiply the force $\\mathbf{F} = {{params.force}} $ to the unit vector of the red vector. </pl-hint>\r\n    <pl-hint level=\"2\" data-type=\"text\">To obtain the unit vector of the red vector, you must identify the location of the head and tail of the red vector. In our case, the tail of the red vector is equal to $ L_2 \\hat{i} + L_1 \\hat{j} + L_3 \\hat{k}$ and the head of the red vector is equal to $ V_2 \\hat{i} + V_1 \\hat{j} + V_3 \\hat{k}$. Now we can find the direction of the red vector by moving from the tail to the head. \r\n        Moving from the tail to the head $ \\implies (V_2 - L_2 ) \\hat{i} + (V_1 - L_1 ) \\hat{j} + (V_3 - L_3) \\hat{k} $. Now that we have the direction we can divide the length of the vector by itself to obtain the unit vector. $ \\frac {(V_2 - L_2 ) \\hat{i} + (V_1 - L_1 ) \\hat{j} + (V_3 - L_3) \\hat{k}}{\\sqrt{(V_2 - L_2 )^2 + (V_1 - L_1 )^2 + (V_3 - L_3)^2}} $\r\n        </pl-hint>\r\n    <pl-hint level=\"3\" data-type=\"text\">\r\n        <ul> \r\n            Now all we have to do is multiply the force by the unit vetcor.\r\n        <li> $\\mathbf{\\vec{F}} =   \\mathbf(F) \\frac {(V_2 - L_2 ) \\hat{i} + (V_1 - L_1 ) \\hat{j} + (V_3 - L_3) \\hat{k}}{\\sqrt{(V_2 - L_2 )^2 + (V_1 - L_1 )^2 + (V_3 - L_3)^2}} $ </li>\r\n        Now that we have the true force vector we can now take the moment about point O using the cross product $M_o = \\vec{d} X \\vec{F} $\r\n        </ul>\r\n    </pl-hint>\r\n\r\n\r\n\r\n    <pl-hint level=\"4\" data-type=\"text\"> \r\n        <ul>\r\n            When computing the moment about point O using the cross product we must chose any distance ($\\vec{d}$) starting from the point O and ending anywhere along the line of action of the force vector.\r\n            In our case we can just use the blue beam since it starts at point o and ends at the tail of the force vector.  \r\n        <li>$\\vec{d} = L_2 \\hat{i} +L_1 \\hat{j} + L_3 \\hat{k}$</li>\r\n        <li>$M_o = \\vec{d} X \\vec{F} $ $\\implies $ $M_o = (L_2, L_1,L_3) X (F_x,F_y,F_z)$ $\\implies $  $M_o = ({{correct_answers.momenti}}) \\hat{i} + ({{correct_answers.momentj}}) \\hat{j} + ({{correct_answers.momentk}}) \\hat{k} $   </li>\r\n        \r\n        </ul>\r\n    </pl-hint>\r\n\r\n\r\n"""
    # Step 1: Replace <pl-question-panel> → <div>
    print("\n[1] Replacing <pl-question-panel> with <div>...")
    pl_panel_replacer = TagReplacer(
        html=html_string,
        target_tag="pl-question-panel",
        replacement_tag="div",
        attributes={"class": "question-panel-wrapper"},
    )
    new_soup = pl_panel_replacer.run()
    print(new_soup.prettify())

    # Step 2: Replace <pl-figure> → <img src="..." class="question-figure">
    print("\n[2] Replacing <pl-figure> with <img>...")
    pl_figure_replacer = TagReplacer(
        html=str(new_soup),
        target_tag="pl-figure",
        replacement_tag="img",
        attributes={"class": "question-figure"},
        mapping={"file-name": "src"},
    )
    new_soup = pl_figure_replacer.run()
    print(new_soup.prettify())

    # Step 3: Replace <pl-answer> → <input type="checkbox" data-correct="...">
    print("\n[3] Replacing <pl-answer> with <input type='checkbox'>...")
    pl_answer_replacer = TagReplacer(
        html=str(new_soup),
        target_tag="pl-answer",
        replacement_tag="input",
        attributes={"type": "checkbox"},
        mapping={"correct": "data-correct"},
    )
    new_soup = pl_answer_replacer.run()
    print(new_soup.prettify())

    # Step 4: Replace <pl-checkbox> → <fieldset>
    print("\n[4] Replacing <pl-checkbox> with <fieldset>...")
    pl_checkbox_replacer = TagReplacer(
        html=str(new_soup),
        target_tag="pl-checkbox",
        replacement_tag="fieldset",
        attributes={"class": "checkbox-group"},
        mapping={
            "answers-name": "answers-name",
            "weight": "data-weight",
            "inline": "data-inline",
        },
    )
    new_soup = pl_checkbox_replacer.run()
    print(new_soup.prettify())

    print("/n test 2")

    from .tag_replacer_config import tag_replacer_configs

    pl_number_input_data = tag_replacer_configs.get("pl_number_input")
    pl_number_input_replacer = TagReplacer(
        html=str(html_string2),
        target_tag=pl_number_input_data.get("target_tag"),
        replacement_tag=pl_number_input_data.get("replacement_tag"),
        attributes=pl_number_input_data.get("attributes"),
        mapping=pl_number_input_data.get("mapping"),
    )
    new_soup = pl_number_input_replacer.run()
    print(new_soup.prettify())

    pl_solution_step_data = tag_replacer_configs.get("pl_hint")
    print("Before :", {html_string3})
    pl_number_input_replacer = TagReplacer(
        html=str(html_string3),
        target_tag=pl_solution_step_data.get("target_tag"),
        replacement_tag=pl_solution_step_data.get("replacement_tag"),
        attributes=pl_solution_step_data.get("attributes"),
        mapping=pl_solution_step_data.get("mapping"),
    )

    new_soup = pl_number_input_replacer.run()
    print(new_soup.prettify())


if __name__ == "__main__":
    main()
