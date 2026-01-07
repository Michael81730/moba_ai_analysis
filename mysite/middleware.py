# myapp/middleware.py
import time
from django.utils.deprecation import MiddlewareMixin

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Store the start time when the request first hits the middleware
        request._start_time = time.time()
        print(f'Incoming Request: {request.method} {request.path} | Headers: {request.headers}')

    def process_response(self, request, response):
        # Calculate duration and log details after the response is generated
        try:
            duration = time.time() - request._start_time
            print(f"Outgoing Response: {request.method} {request.path} | Status: {response.status_code} | Response Headers: {response.headers} | Response cookies: {response.cookies}")
        except AttributeError:
            # Handle cases where process_request might not have run (e.g., a middleware before this one returned a response)
            print(f"Outgoing Response: {request.method} {request.path} | Status: {response.status_code} | Response Headers: {response.headers} | Response cookies: {response.cookies}")
        return response