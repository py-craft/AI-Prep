from fastapi import APIRouter

from ..dependencies import OrderServiceDep
from ..schemas import OrderQuestion, SupportAnswer


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/ask", response_model=SupportAnswer)
async def ask_order(
    request: OrderQuestion,
    service: OrderServiceDep,
) -> SupportAnswer:
    return await service.answer(request.question)
