from fastapi import FastAPI, Request, HTTPException
from slowapi.middleware import SlowAPIMiddleware
import yaml

from api.middleware.host_restriction import restrict_host_header
from api.middleware.rate_limiter import init_rate_limiter

from api.routes.countries import router as countries_router
from api.routes.states import router as states_router
from api.routes.cities import router as cities_router

with open("api/config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)
    
allowed_hosts = config.get("allowed_hosts", ["*"])
if len(allowed_hosts) == 0:
    allowed_hosts = ["*"]

rate_limit = config.get("rate_limit", {}).get("limit", "100/hour")

# Initialize app
app = FastAPI()

# Initialize rate limiter
limiter = init_rate_limiter(rate_limit)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.middleware("http")
async def restrict_host(request: Request, call_next):
    return await restrict_host_header(request, call_next, allowed_hosts)

# Inlude routes
app.include_router(countries_router, prefix="/api", tags=["Countries"])
app.include_router(states_router, prefix="/api", tags=["States"])
app.include_router(cities_router, prefix="/api", tags=["Cities"])

@app.get("/")
def welcome():
    """
    Root endpoint that returns a welcome message.
    
    Returns (dict): A welcome message.
    """
    return { "message": "Welcome to the World API!" }
