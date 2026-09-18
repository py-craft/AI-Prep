from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate

from .prompt_loader import OrderPrompts
from .repositories import OrderToolRepository
from .schemas import SupportAnswer


class OrderAssistantService:
    """Application use case: answer one order question with an MCP tool."""

    def __init__(
        self,
        llm: BaseChatModel,
        repository: OrderToolRepository,
        prompts: OrderPrompts,
    ) -> None:
        self._llm = llm
        self._repository = repository
        self._prompts = prompts

    async def answer(self, question: str) -> SupportAnswer:
        prompt = ChatPromptTemplate.from_messages(
            [("system", self._prompts.system), ("human", "{question}")]
        )
        messages = prompt.invoke({"question": question}).to_messages()

        tools = await self._repository.get_tools()
        tool_map = {tool.name: tool for tool in tools}
        model_with_tools = self._llm.bind_tools(tools).with_retry(
            stop_after_attempt=3
        )
        first_response = await model_with_tools.ainvoke(messages)
        messages.append(first_response)

        for call in first_response.tool_calls:
            tool = tool_map.get(call["name"])
            if tool is None:
                messages.append(
                    ToolMessage(
                        content="Tool unavailable",
                        tool_call_id=call["id"],
                        status="error",
                    )
                )
            else:
                messages.append(await tool.ainvoke(call))

        messages.append(HumanMessage(content=self._prompts.final_answer))
        structured_llm = self._llm.with_structured_output(SupportAnswer).with_retry(
            stop_after_attempt=3
        )
        return await structured_llm.ainvoke(messages)
