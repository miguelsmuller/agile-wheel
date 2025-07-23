from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

PUBLIC_PATHS = {}


class APITokenMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, token: str) -> None:
        super().__init__(app)
        self.token = token

    async def dispatch(self, request: Request, call_next):
        # 1º - Every OPTIONS request is allowed (CORS pre-flight)
        if request.method == "OPTIONS":
            return await call_next(request)

        # 2º - Public paths do not require token validation
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        # 3º - If request is from a browser (Origin header), allow
        is_browser = "mozilla" in request.headers.get("user-agent", "").lower()
        has_origin = request.headers.get("origin") is not None
        if is_browser or has_origin:
            return await call_next(request)

        # then - If the token is required, validate it
        provided = request.headers.get("x-api-token")
        if not self.token or provided == self.token:
            return await call_next(request)

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid API token"},
        )
