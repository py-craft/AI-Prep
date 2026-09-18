from fastapi import FastAPI

from .api.routes import router
from .config import get_settings
from .prompt_loader import get_order_prompts


# Fail during startup/import instead of on the first request.
get_settings()
get_order_prompts()

app = FastAPI(title="Lesson 4 Order Assistant", version="1.0.0")
app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
