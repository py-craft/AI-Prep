from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class OrderPrompts(BaseModel):
    """Validated prompt configuration loaded from YAML."""

    system: str = Field(min_length=1)
    final_answer: str = Field(min_length=1)


@lru_cache
def get_order_prompts() -> OrderPrompts:
    prompt_path = Path(__file__).parent / "prompts" / "order_assistant.yml"
    if not prompt_path.is_file():
        raise FileNotFoundError(f"Missing prompt file: {prompt_path}")

    with prompt_path.open(encoding="utf-8") as prompt_file:
        raw_prompts = yaml.safe_load(prompt_file)

    return OrderPrompts.model_validate(raw_prompts)
