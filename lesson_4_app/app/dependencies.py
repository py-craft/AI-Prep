from typing import Annotated

from fastapi import Depends
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from .config import Settings, get_settings
from .prompt_loader import OrderPrompts, get_order_prompts
from .repositories import OrderToolRepository
from .services import OrderAssistantService


SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_llm(settings: SettingsDep) -> BaseChatModel:
    return ChatOpenAI(
        api_key=settings.openai_api_key,
        model=settings.model,
        use_responses_api=True,
    )


LlmDep = Annotated[BaseChatModel, Depends(get_llm)]


def get_repository(settings: SettingsDep) -> OrderToolRepository:
    return OrderToolRepository(settings.mcp_url)


RepositoryDep = Annotated[OrderToolRepository, Depends(get_repository)]
PromptsDep = Annotated[OrderPrompts, Depends(get_order_prompts)]


def get_order_service(
    llm: LlmDep,
    repository: RepositoryDep,
    prompts: PromptsDep,
) -> OrderAssistantService:
    return OrderAssistantService(llm=llm, repository=repository, prompts=prompts)


OrderServiceDep = Annotated[OrderAssistantService, Depends(get_order_service)]
