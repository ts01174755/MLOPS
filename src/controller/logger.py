import logging
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logging.info(f"Request: {request.method} {request.url}")
        response: Response = await call_next(request)
        logging.info(f"Response: {response.status_code}")
        return response
