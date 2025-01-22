from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yaml

from api.routes.countries import router as countries_router
from api.routes.states import router as states_router
from api.routes.cities import router as cities_router

with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)
    
allowed_origins = config["allowed_origins"]

if not allowed_origins or len(allowed_origins) == 0:
    allowed_origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(countries_router, prefix="/api", tags=["Countries"])
app.include_router(states_router, prefix="/api", tags=["States"])
app.include_router(cities_router, prefix="/api", tags=["Cities"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the World API!"}