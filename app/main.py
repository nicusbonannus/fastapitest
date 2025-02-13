from fastapi import FastAPI

from app.routes.journeys import router
from app.settings import DEBUG

app = FastAPI(debug=DEBUG)

app.include_router(router, prefix="/journeys", tags=["journeys"])
