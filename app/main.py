from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import notifications
from app.db.base import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Include routers
app.include_router(notifications.router, prefix=settings.API_V1_STR)
