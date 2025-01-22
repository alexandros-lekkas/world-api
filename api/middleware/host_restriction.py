from fastapi import Request, HTTPException
from starlette.responses import JSONResponse

async def restrict_host_header(request: Request, call_next, allowed_hosts):
    """
    Middleware that restricts the Host header to the allowed origins.
    
    Args:
        request (Request): The request object.
        call_next (function): The next middleware function.
        allowed_hosts (list): A list of allowed hosts.
    
    Returns (Response): The response object.
    """
    host = request.headers.get("host")
    print("Host:", host)
    
    if host not in allowed_hosts and "*" not in allowed_hosts:
        return JSONResponse(content={"detail": "Host header invalid."}, status_code=400)
    
    return await call_next(request)
