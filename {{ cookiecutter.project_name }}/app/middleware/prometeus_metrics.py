from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Summary
from datetime import datetime
import logging

from app.metrics.prometeus import REQUEST_COUNT, REQUEST_LATENCY

logger = logging.getLogger(__name__)


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = datetime.now()
        response = await call_next(request)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status_code=response.status_code).inc()
        REQUEST_LATENCY.observe(duration)

        logger.trace("Request %s %s took %s seconds", request.method, request.url.path, duration)
        return response