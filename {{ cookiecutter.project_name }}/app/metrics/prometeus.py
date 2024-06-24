# metrics.py
from prometheus_client import start_http_server, Counter, Summary

import logging
logger = logging.getLogger(__name__)

# Définir des métriques
REQUEST_COUNT = Counter('http_requests_total', 'Total number of HTTP requests', ['method', 'endpoint', 'status_code'])
REQUEST_LATENCY = Summary('http_request_duration_seconds', 'Time spent processing request')

def start_prometheus_server(settings):
    """
    Start the Prometheus server.

    :param settings: Application settings containing the Prometheus port
    """
    logger.trace("Starting Prometheus server on port %s", settings.PROMETHEUS_PORT)
    start_http_server(settings.PROMETHEUS_PORT)