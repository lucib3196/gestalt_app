from .TagReplacer import TagReplacer
from typing import Dict, List
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