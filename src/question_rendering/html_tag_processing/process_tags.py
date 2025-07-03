
from __future__ import annotations
from typing import Generator, Iterable
from bs4 import BeautifulSoup
from question_rendering.html_tag_processing.load_tag_replacer import (
    load,
)
from .tag_replacer import TagReplacer, TagConfig


def apply_all_replacers(
    html: str | BeautifulSoup,
    tag_configs: Iterable[TagConfig] | None = None,
    *,
    show_steps: bool = False,
) -> BeautifulSoup:
    """
    Apply **every** `TagReplacer` found in `tag_configs` (or via `load()`)
    to the same BeautifulSoup tree, returning the fully-transformed soup.

    Parameters
    ----------
    html
        Raw HTML (string) **or** an existing `BeautifulSoup` object.
    tag_configs
        If provided, use these configs instead of the default `load()`.
    show_steps
        When *True*, prints each intermediate state to stdout.

    Returns
    -------
    BeautifulSoup
        The soup after *all* replacements.
    """
    soup = (
        html if isinstance(html, BeautifulSoup) else BeautifulSoup(html, "html.parser")
    )
    tag_configs = tag_configs or load() # type: ignore

    for idx, cfg in enumerate(tag_configs, 1): # type: ignore
        soup = TagReplacer(soup, cfg).transform()  # reuse the same tree
        if show_steps:
            print(
                f"\n--- After TagConfig #{idx} ({cfg.target_tag}→{cfg.replacement_tag}) ---"
            )
            print(soup.prettify())

    return soup


def iter_replacements(
    html: str | BeautifulSoup,
    tag_configs: Iterable[TagConfig] | None = None,
) -> Generator[BeautifulSoup, None, None]:
    """
    Generator version: yields the soup after each individual replacement.
    Useful for debugging / testing.

    Example
    -------
    >>> for step, soup in enumerate(iter_replacements(raw_html), 1):
    ...     print(f"Step {step}: {len(soup.find_all())} nodes")
    """
    soup = (
        html if isinstance(html, BeautifulSoup) else BeautifulSoup(html, "html.parser")
    )
    tag_configs = tag_configs or load() # type: ignore

    for cfg in tag_configs: # type: ignore
        soup = TagReplacer(soup, cfg).transform()
        yield soup


from pathlib import Path

if __name__ == "__main__":
    
    raw_html = Path(
        "generated_question/BendingStressInSimplySupportedBeam/question.html"
    ).read_text()

    clean_soup = apply_all_replacers(raw_html, show_steps=True)  # prints every stage
    print(clean_soup)
