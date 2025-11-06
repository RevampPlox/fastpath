from fastapi import FastAPI

from app.api.v1.routers import health_check_router

app = FastAPI()
app.include_router(health_check_router.router)
