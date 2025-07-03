from __future__ import annotations

import argparse
import logging
from copy import copy
from pathlib import Path
from typing import Any, Mapping, Union

from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString

# ─────────────────────────────────────────────────────────────────────────────
# Configure logging (caller can override)
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------- #
# Public data model – keeps this class decoupled from any particular project
# --------------------------------------------------------------------------- #
class TagConfig:  # minimal stub; swap with your project’s implementation
    """Configuration that describes how a tag should be transformed."""

    def __init__(
        self,
        target_tag: str,
        replacement_tag: str,
        mapping: Mapping[str, str] | None = None,
        attributes: Mapping[str, str] | None = None,
    ) -> None:
        self.target_tag: str = target_tag
        self.replacement_tag: str = replacement_tag
        self.mapping: Mapping[str, str] = mapping or {}
        self.attributes: Mapping[str, str] = attributes or {}


# --------------------------------------------------------------------------- #
# Core helper
# --------------------------------------------------------------------------- #
class TagReplacer:
    """
    Replace all occurrences of a *target* HTML tag with a *replacement* tag,
    remapping / merging attributes in the process.

    Example
    -------
    ```python
    replacer = TagReplacer("<foo a='1'/>", TagConfig("foo", "bar"))
    new_html = replacer.transform().prettify()
    ```
    """

    # Public API -------------------------------------------------------------
    def __init__(self, html: str | BeautifulSoup, config: Any) -> None:
        self.soup: BeautifulSoup = (
            html
            if isinstance(html, BeautifulSoup)
            else BeautifulSoup(html, "html.parser")
        )
        self.config = config

    def transform(self) -> BeautifulSoup:
        """Apply the configured tag replacement to *all* matching elements."""
        for tag in self.soup.find_all(self.config.target_tag):
            if not isinstance(tag, Tag):  # pragma: no cover – defensive
                continue

            mapped_attrs = self._map_attributes(tag.attrs)
            merged_attrs = {**self.config.attributes, **mapped_attrs}

            new_tag = self.soup.new_tag(self.config.replacement_tag, attrs=merged_attrs)

            # Copy children, skipping pure-whitespace strings
            for child in tag.children:  # type: ignore
                if isinstance(child, NavigableString) and not child.strip():
                    continue
                new_tag.append(copy(child))

            tag.replace_with(new_tag)
            self._inject_label(new_tag, merged_attrs)

        return self.soup

    # Internals --------------------------------------------------------------
    def _map_attributes(self, old_atts: Mapping[str, Any]) -> dict[str, Any]:
        """Translate attributes according to `config.mapping`."""
        new_attrs = {
            new_key: old_atts[old_key]
            for old_key, new_key in self.config.mapping.items()
            if old_key in old_atts
        }
        unmapped = set(old_atts) - set(self.config.mapping)
        if unmapped:
            logger.debug("Unmapped attributes encountered: %s", unmapped)
        return new_attrs

    def _inject_label(self, new_tag: Tag, attrs: Mapping[str, str]) -> None:
        """Optionally wrap the new tag in a <label> if `label` attr present."""
        label_text = attrs.get("label")
        if not label_text:
            return

        label_wrapper = self.soup.new_tag(
            "label",
            attrs={"class": f"{self.config.target_tag}-label"},
        )
        label_wrapper.string = label_text
        new_tag.wrap(label_wrapper)


# --------------------------------------------------------------------------- #
# CLI utility (optional)
# --------------------------------------------------------------------------- #
def _cli() -> None:
    parser = argparse.ArgumentParser(description="Replace HTML tags in a file.")
    parser.add_argument(
        "html_file", type=Path, help="Path to the HTML file to process."
    )
    args = parser.parse_args()

    html_src = args.html_file.read_text(encoding="utf-8")

    # Example: load your TagConfig list however you like
    from question_rendering.html_tag_processing.load_tag_replacer import (
        load,
    )  # local project import

    for idx, cfg in enumerate(load(), 1):
        replacer = TagReplacer(html_src, cfg)
        transformed = replacer.transform()
        logger.info("Result for TagConfig #%d\n%s\n", idx, "-" * 40)
        print(transformed.prettify())  # or write back to disk

    logger.info("Done.")


if __name__ == "__main__":
    _cli()
