import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("request")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()

        response = await call_next(request)

        process_time = round(time.time() - start, 3)

        logger.info(
            "%s %s -> %s (%ss)",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )

        return response