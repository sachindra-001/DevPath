"""CSRF protection middleware (DESIGN.md §23.3).

Requires `X-Requested-With: fetch` on state-changing HTTP methods.
"""

from collections.abc import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class CSRFMiddleware(BaseHTTPMiddleware):
    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
    EXEMPT_PATHS = {"/api/docs", "/api/openapi.json", "/api/v1/healthz"}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.method not in self.SAFE_METHODS and request.url.path not in self.EXEMPT_PATHS:
            header_val = request.headers.get("X-Requested-With")
            if not header_val or header_val.lower() != "fetch":
                # Allow if Authorization header is present (non-browser tools/tests with Bearer)
                auth_header = request.headers.get("Authorization")
                if not auth_header:
                    return JSONResponse(
                        status_code=403,
                        content={
                            "error": {
                                "code": "csrf_validation_failed",
                                "message": "Missing or invalid 'X-Requested-With: fetch' header.",
                            }
                        },
                    )

        return await call_next(request)
