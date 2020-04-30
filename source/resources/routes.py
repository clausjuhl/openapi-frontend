from starlette.routing import Route
from source.resources import views

routes = [
    Route(
        "/{collection}/{item:int}",
        views.resource,
        name="resource",
        methods=["GET", "POST"],
    )
]
