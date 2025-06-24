from typing import Dict, Optional
from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString
from copy import copy
from typing import Union
from pydantic import BaseModel


class TagConfig(BaseModel):
    target_tag: str
    replacement_tag: str
    attributes: dict[str, str]
    mapping: dict


class TagReplacer:
    def __init__(self, html: Union[str, BeautifulSoup], tag_configuration: TagConfig):
        if isinstance(html, BeautifulSoup):
            self.soup = html
        else:
            self.soup = BeautifulSoup(html.replace('\\"', '"'), "html.parser")
        self.tag_configuration = tag_configuration

    def replace_tag(self) -> BeautifulSoup:

        for tag in self.soup.find_all(self.tag_configuration.target_tag):
            print(tag)
