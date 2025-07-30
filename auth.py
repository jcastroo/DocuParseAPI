from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

RAPIDAPI_KEYS = {
    "your-free-user-key": {"plan": "free", "limit": 100},
    "your-pro-user-key": {"plan": "pro", "limit": 10000},
}

request_counts = {}

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("X-RapidAPI-Key")
        
        if not api_key or api_key not in RAPIDAPI_KEYS:
            raise HTTPException(status_code=401, detail="Invalid or missing API Key")

        count = request_counts.get(api_key, 0)
        limit = RAPIDAPI_KEYS[api_key]["limit"]
        if count >= limit:
            raise HTTPException(status_code=429, detail="API rate limit exceeded")

        request_counts[api_key] = count + 1
        request.state.plan = RAPIDAPI_KEYS[api_key]["plan"]

        return await call_next(request)
