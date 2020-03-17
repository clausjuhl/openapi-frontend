import uvicorn

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from source import endpoints, settings, routes

middleware = [
    Middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,
        https_only=settings.HTTPS_ONLY,
    )
]
if settings.HTTPS_ONLY:
    middleware += [Middleware(HTTPSRedirectMiddleware)]

exception_handlers = {404: endpoints.not_found, 500: endpoints.server_error}

app = Starlette(
    debug=settings.DEBUG,
    routes=routes.routes,
    middleware=middleware,
    exception_handlers=exception_handlers,
    on_startup=[],
    on_shutdown=[],
)
