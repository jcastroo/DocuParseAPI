from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

API_KEYS = {
    "free-key-123": {"plan": "free", "limit": 100},
    "pro-key-abc": {"plan": "pro", "limit": 10000},
}

request_counts = {}

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("X-API-Key")
        if not api_key or api_key not in API_KEYS:
            raise HTTPException(status_code=401, detail="Invalid or missing API Key")

        count = request_counts.get(api_key, 0)
        limit = API_KEYS[api_key]["limit"]
        if count >= limit:
            raise HTTPException(status_code=429, detail="API rate limit exceeded")
        
        request_counts[api_key] = count + 1

        request.state.plan = API_KEYS[api_key]["plan"]

        response = await call_next(request)
        return response
