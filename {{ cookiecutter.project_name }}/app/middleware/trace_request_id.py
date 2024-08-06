from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import uuid
import logging
from app.config.context_variables import trace_id_var

# Configure logger
logger = logging.getLogger(__name__)


class TraceIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add a unique request ID to each request and response.

    The request ID is added to the request state and response headers.
    """

    async def dispatch(self, request: Request, call_next):
        trace_id = str(uuid.uuid4())
        trace_id_var.set(trace_id)
        request.state.trace_id = trace_id
        logger.debug("Generated Trace ID: %s for request", trace_id)

        response = await call_next(request)
        response.headers["X-Trace-ID"] = trace_id
        return response
