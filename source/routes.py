from starlette.routing import Route, Mount
from source import endpoints
from source.staticfiles import statics

routes = [
    Route("/", endpoints.index, name="homepage", methods=["GET"]),
    Route("/500", endpoints.error(500), name="errortest"),
    Mount("/static", statics, name="static"),
    # Mount("/auth", routes=auth_routes, name='auth'),
]
