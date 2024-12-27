from fastapi import FastAPI
from app.routes.journeys import router

app = FastAPI()

app.include_router(router, prefix="/journeys", tags=["journeys"])
