import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from dotenv import dotenv_values, load_dotenv


@dataclass(frozen=True)
class Settings:
    openai_api_key: str = field(repr=False)
    mcp_url: str = "http://127.0.0.1:8000/mcp"
    model: str = "gpt-5.6-luna"


@lru_cache
def get_settings() -> Settings:
    dotenv_path = Path(__file__).resolve().parents[2] / ".env"
    if not dotenv_path.is_file():
        raise FileNotFoundError(
            f"Missing {dotenv_path}. Create it with OPENAI_API_KEY=your-key."
        )

    values = dotenv_values(dotenv_path)
    api_key = values.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(f"OPENAI_API_KEY is missing or empty in {dotenv_path}.")

    # Runtime environment variables (for example, Compose configuration) win.
    load_dotenv(dotenv_path, override=False)
    return Settings(
        openai_api_key=api_key,
        mcp_url=os.getenv("MCP_URL", "http://127.0.0.1:8000/mcp"),
        model=os.getenv("OPENAI_MODEL", "gpt-5.6-luna"),
    )
