"""FastAPI application entrypoint with Scalar docs."""

from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from scalar_fastapi import get_scalar_documentation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from infrastructure.db.session import get_session
from presentation.api.v1.routes_activities import router as activities_router
from presentation.api.v1.routes_customers import router as customers_router
from presentation.api.v1.routes_deals import router as deals_router
from presentation.api.v1.routes_tasks import router as tasks_router
from settings import get_settings


settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0", docs_url=None, redoc_url=None)
app.add_route("/docs", get_scalar_documentation(app), include_in_schema=False)


@app.get("/health")
async def health(session: AsyncSession = Depends(get_session)) -> dict[str, str]:
    try:
        await session.execute(text("SELECT 1"))
    except Exception as exc:  # pragma: no cover - health is best-effort
        raise HTTPException(status_code=500, detail=str(exc))
    return {"status": "ok"}


app.include_router(customers_router)
app.include_router(activities_router)
app.include_router(deals_router)
app.include_router(tasks_router)
