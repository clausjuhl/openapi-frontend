from starlette.routing import Route, Mount

from source import views
from source.staticfiles import statics

routes = [
    Route("/", views.index, name="homepage", methods=["GET"]),
    Route("/500", views.error(500), name="errortest"),
    Mount("/static", statics, name="static"),
    # Mount("/auth", routes=auth_routes, name='auth'),
]
