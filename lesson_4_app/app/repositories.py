from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient


class OrderToolRepository:
    """Data-access boundary for the external order MCP server."""

    def __init__(self, mcp_url: str) -> None:
        self._client = MultiServerMCPClient(
            {
                "orders": {
                    "transport": "http",
                    "url": mcp_url,
                }
            }
        )

    async def get_tools(self) -> list[BaseTool]:
        return await self._client.get_tools()
