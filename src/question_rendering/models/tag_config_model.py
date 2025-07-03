from pydantic import BaseModel


class TagConfig(BaseModel):
    target_tag: str
    replacement_tag: str
    attributes: dict[str, str]
    mapping: dict
