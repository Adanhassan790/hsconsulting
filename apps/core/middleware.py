"""
Middleware for improved error logging and diagnostics in production
"""
import logging
import traceback
from django.http import HttpResponse

logger = logging.getLogger(__name__)


class ProductionErrorLoggingMiddleware:
    """
    Logs all errors and exceptions in production for easier debugging
    Helps diagnose why latest code changes aren't showing
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            
            # Log 5xx errors
            if response.status_code >= 500:
                logger.error(
                    f"[PRODUCTION_ERROR] {response.status_code} response",
                    extra={
                        'path': request.path,
                        'method': request.method,
                        'status_code': response.status_code,
                    }
                )
            
            return response
            
        except Exception as e:
            # Log the exception with full traceback
            logger.exception(
                f"[PRODUCTION_ERROR] Unhandled exception: {type(e).__name__}",
                extra={
                    'path': request.path,
                    'method': request.method,
                    'exception': str(e),
                    'traceback': traceback.format_exc(),
                }
            )
            
            # Return a helpful error page
            error_html = f"""
            <html>
            <head>
                <title>Server Error</title>
                <style>
                    body {{ font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
                    .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                    h1 {{ color: #e74c3c; }}
                    code {{ background: #ecf0f1; padding: 2px 6px; border-radius: 3px; }}
                    .debug-info {{ background: #f9f9f9; padding: 15px; margin: 20px 0; border-left: 3px solid #3498db; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Error Processing Request</h1>
                    <p><strong>Error Type:</strong> {type(e).__name__}</p>
                    <p><strong>Error Message:</strong> {str(e)}</p>
                    <p><strong>Path:</strong> {request.path}</p>
                    <p><strong>Method:</strong> {request.method}</p>
                    
                    <div class="debug-info">
                        <p><strong>Debug Links:</strong></p>
                        <ul>
                            <li><a href="/deploy-info/">View Deployment Info</a> - Shows git commit, static files, templates</li>
                            <li><a href="/health/">Health Check</a> - Database and system status</li>
                            <li><a href="/test/">Server Test</a> - Basic connectivity test</li>
                            <li><a href="/admin/">Django Admin</a> - Admin interface</li>
                        </ul>
                    </div>
                    
                    <p>The error has been logged. An admin has been notified.</p>
                </div>
            </body>
            </html>
            """
            
            return HttpResponse(error_html, status=500, content_type='text/html')


class RequestLoggingMiddleware:
    """Log all incoming requests with details"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Log request
        logger.info(
            f"[REQUEST] {request.method} {request.path}",
            extra={
                'method': request.method,
                'path': request.path,
                'remote_addr': request.META.get('REMOTE_ADDR'),
                'user_agent': request.META.get('HTTP_USER_AGENT', '')[:100],
            }
        )
        
        response = self.get_response(request)
        
        # Log response
        logger.info(
            f"[RESPONSE] {request.method} {request.path} -> {response.status_code}",
            extra={
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
            }
        )
        
        return response
