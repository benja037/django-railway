import logging

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request details
        logger.info(f'HTTP {request.method} Request to {request.path} from {request.META.get("REMOTE_ADDR")}')
        logger.info(f'Headers: {request.headers}')
        if request.method in ('POST', 'PUT', 'PATCH'):
            logger.info(f'Body: {request.body}')

        response = self.get_response(request)

        # Log the response details
        logger.info(f'HTTP {response.status_code} Response from {request.path}')

        return response
