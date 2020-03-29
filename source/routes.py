from starlette.routing import Route, Mount

from source import views
from source.staticfiles import statics

routes = [
    Route("/", views.index, name="home", methods=["GET"]),
    Route(
        "/resource/{collection}/{item:int}",
        views.resource,
        name="resource",
        methods=["GET"],
    ),
    Mount("/static", statics, name="static"),
    # Mount("/auth", routes=auth_routes, name='auth'),
]
