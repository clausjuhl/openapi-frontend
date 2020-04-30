from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

# from source.views import error
from source.routes import routes
from source.database import database
from source import configuration

# Middleware
allowed_hosts = ["*"]
middleware = [
    Middleware(
        SessionMiddleware,
        secret_key=configuration.SECRET_KEY,
        same_site="Lax",  # Lax is default
        https_only=configuration.HTTPS_ONLY,
    ),
    Middleware(GZipMiddleware),
    Middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts),
]
if configuration.HTTPS_ONLY:
    middleware += [Middleware(HTTPSRedirectMiddleware)]

# Exceptions
# exception_handlers = {404: error(404), 500: error(500)}

app = Starlette(
    debug=configuration.DEBUG,
    routes=routes,
    middleware=middleware,
    # exception_handlers=exception_handlers,
    on_startup=[database.connect],
    on_shutdown=[database.disconnect],
)

# uvicorn  --reload --port 5000 --host 0.0.0.0 --env-file .env source.app:app
