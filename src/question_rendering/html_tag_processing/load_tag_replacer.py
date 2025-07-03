from .tag_replace_config import tag_replacer_configs
from question_rendering.models import TagConfig


def load():
    return [TagConfig(**cfg) for name, cfg in tag_replacer_configs.items()]


if __name__ == "__main__":
    print(load())
