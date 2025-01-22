from fastapi import FastAPI, Request, HTTPException
import yaml

from api.routes.countries import router as countries_router
from api.routes.states import router as states_router
from api.routes.cities import router as cities_router

with open("api/config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)
    
allowed_hosts= config["allowed_hosts"]

if (not allowed_hosts) or len(allowed_hosts) == 0:
    allowed_hosts = ["*"]

app = FastAPI()

app.include_router(countries_router, prefix="/api", tags=["Countries"])
app.include_router(states_router, prefix="/api", tags=["States"])
app.include_router(cities_router, prefix="/api", tags=["Cities"])

@app.middleware("http")
async def restrict_host_header(request: Request, call_next):
    """
    Middleware that restricts the Host header to the allowed origins.
    
    Args:
        request (Request): The request object.
        call_next (function): The next middleware function.
    
    Returns (Response): The response object.
    """
    host = request.headers.get("host")
    
    if host not in allowed_hosts and "*" not in allowed_hosts:
        raise HTTPException(status_code=400, detail="Host header invalid.")
    
    response = await call_next(request)
    return response

@app.get("/")
def welcome():
    """
    Root endpoint that returns a welcome message.
    
    Returns (dict): A welcome message.
    """
    return {"message": "Welcome to the World API!"}
