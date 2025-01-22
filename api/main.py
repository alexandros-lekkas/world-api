from fastapi import FastAPI, HTTPException

from api.routes.countries import router as countries_router

app = FastAPI()

app.include_router(countries_router, prefix="/api", tags=["Countries"])
