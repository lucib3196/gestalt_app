from typing import Dict, Optional
from bs4 import BeautifulSoup, Tag


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
        mapping: Optional[Dict[str, str]] = None
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
        self.soup: BeautifulSoup = BeautifulSoup(self.html, "html.parser")

    def map_attributes(self, old_attrs: Dict[str, str], mapping: Dict[str, str]) -> Dict[str, str]:
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
        for tag in self.soup.find_all(self.target_tag):
            mapped_attrs = self.map_attributes(tag.attrs, self.mapping)
            merged_attrs = {**self.attributes, **mapped_attrs}
            new_tag = self.soup.new_tag(name=self.replacement_tag, attrs=merged_attrs)

            for child in tag.contents:
                new_tag.append(child)

            tag.replace_with(new_tag)

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
            new_tag = self.soup.new_tag(name=self.replacement_tag, attrs=merged_attrs)

            for child in list(tag.children):
                new_tag.append(child.extract())

            tag.replace_with(new_tag)

        return self.soup

    def run(self) -> BeautifulSoup:
        """
        Run the replacer logic based on number of matches found.

        Returns:
            BeautifulSoup: The final modified soup.
        """
        try:
            tags = self.soup.find_all(self.target_tag)
            if not tags:
                print(f"[Info] No tags found for <{self.target_tag}>.")
                return self.soup
            elif len(tags) == 1:
                return self.replace_tag_unique()
            else:
                return self.replace_tag()
        except Exception as e:
            print(f"[Error] Could not process <{self.target_tag}>: {e}")
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

    # Step 1: Replace <pl-question-panel> → <div>
    print("\n[1] Replacing <pl-question-panel> with <div>...")
    pl_panel_replacer = TagReplacer(
        html=html_string,
        target_tag="pl-question-panel",
        replacement_tag="div",
        attributes={"class": "question-panel-wrapper"}
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
        mapping={"file-name": "src"}
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
        mapping={"correct": "data-correct"}
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
            "inline": "data-inline"
        }
    )
    new_soup = pl_checkbox_replacer.run()
    print(new_soup.prettify())


if __name__ == "__main__":
    main()
