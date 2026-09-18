"""FastMCP order service shared by Lessons 2 and 3."""

import os
from typing import Literal

from fastmcp import FastMCP
from pydantic import BaseModel, Field


ORDER_DATABASE = {
    "A100": "shipped",
    "B200": "processing",
}


class OrderStatus(BaseModel):
    """Validated order-status result returned by the MCP tool."""

    order_id: str = Field(description="Order identifier supplied by the user")
    status: Literal["shipped", "processing", "not_found"]


order_mcp = FastMCP(
    "Order Service",
    instructions="Use get_order_status for factual order-status lookups.",
)


@order_mcp.tool
def get_order_status(order_id: str) -> OrderStatus:
    """Return the trusted status for one order."""
    status = ORDER_DATABASE.get(order_id, "not_found")
    return OrderStatus(order_id=order_id, status=status)


@order_mcp.resource("orders://policy")
def order_policy() -> str:
    """Explain the meanings of order statuses."""
    return (
        "shipped: handed to carrier; "
        "processing: being prepared; "
        "not_found: no matching order"
    )


@order_mcp.prompt
def investigate_order(order_id: str) -> str:
    """Create a reusable request for an order investigation."""
    return (
        f"Check order {order_id} with get_order_status, then explain "
        "the result clearly without inventing missing details."
    )


if __name__ == "__main__":
    order_mcp.run(
        transport="http",
        host=os.getenv("MCP_HOST", "127.0.0.1"),
        port=int(os.getenv("MCP_PORT", "8000")),
    )
