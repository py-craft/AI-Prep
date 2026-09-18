from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class OrderQuestion(BaseModel):
    """Validated HTTP input."""

    model_config = ConfigDict(str_strip_whitespace=True)

    question: str = Field(min_length=3, max_length=500)


class SupportAnswer(BaseModel):
    """Validated LLM and HTTP output."""

    answer: str = Field(min_length=1)
    status: Literal["shipped", "processing", "not_found", "unknown"]
    grounded: bool = Field(
        description="True only when the status came from a successful MCP tool call"
    )
