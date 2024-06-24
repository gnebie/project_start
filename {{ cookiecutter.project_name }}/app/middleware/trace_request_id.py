from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import uuid
import logging

# Configure logger
logger = logging.getLogger(__name__)

class TraceIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add a unique request ID to each request and response.

    The request ID is added to the request state and response headers.
    """
    async def dispatch(self, request: Request, call_next):
        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id
        logger.trace("Generated Trace ID: %s for request", trace_id)
        response = await call_next(request)
        response.headers["X-Trace-ID"] = trace_id
        return response