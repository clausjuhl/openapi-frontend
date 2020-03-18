import uvicorn

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from source import endpoints, settings, routes

allowed_hosts = ["*"]
middleware = [
    Middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,
        same_site="Lax",  # default
        https_only=settings.HTTPS_ONLY,
    ),
    Middleware(GZipMiddleware),
    Middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts),
]
if settings.HTTPS_ONLY:
    middleware += [Middleware(HTTPSRedirectMiddleware)]

exception_handlers = {404: endpoints.error(404), 500: endpoints.error(500)}

app = Starlette(
    debug=settings.DEBUG,
    routes=routes.routes,
    middleware=middleware,
    exception_handlers=exception_handlers,
    on_startup=[],
    on_shutdown=[],
)
