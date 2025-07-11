from fastapi import Request, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
from pydantic import BaseModel
import os
from utils.manage_auth import decode_access_token
from exceptions.models import CustomError
from urllib.parse import urlparse

# Define security scheme
security = HTTPBearer(auto_error=False)

# Define excluded routes that don't require authentication
PUBLIC_ROUTES = {
    # "/api/v1/users/add-user",
    "/api/v1/users/login"  ,
    "/api/v1/vehicles/add-vehicle" , 
    "/api/v1/vehicles/update-vehicle",
    "/api/v1/files/get",
    "/api/v1/files/send-video-stream",
    "/api/v1/files/get-video-stream"
}

# Define the user payload structure
class TokenData(BaseModel):
    email: str
    id: str
    role: str

async def authenticate_user(
    request: Request, credentials: HTTPAuthorizationCredentials = Security(security)
):
    """Middleware-style function for authenticating users before hitting the router."""
    # path = request.url.path 

    path = urlparse(request.url.path).path  # Extract path without query parameters
    print("path: ", path)
    # Skip authentication for public routes
    if path in PUBLIC_ROUTES:
        return

    # Extract JWT from the Authorization header
    token = credentials.credentials if credentials else None
    if not token:
        raise CustomError(message= "access_token is required", status_code=403, resolution="please provide a token")

    # Decode and validate the token
    token_data = decode_access_token(token)

    auth=token_data["auth"]
    if not auth:
        raise CustomError(message= "no enough data has provided in this token", status_code=401)
    # Validate required claims
    if not all(k in auth for k in ["email", "id", "role"]):
        raise CustomError(message= "no enough data has provided in this token", status_code=401)

    # Attach user data to the request for further use
    request.state.user = auth
