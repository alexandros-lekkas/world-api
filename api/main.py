from fastapi import FastAPI, HTTPException

from api.routes.countries import router as countries_router
from api.routes.states import router as states_router

app = FastAPI()

app.include_router(countries_router, prefix="/api", tags=["Countries"])
app.include_router(states_router, prefix="/api", tags=["States"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the World API!"}