from starlette.routing import Route
from source.resources import views

routes = [
    Route(
        "/{collection}/{item:int}",
        views.resource,
        name="resource",
        methods=["GET", "POST"],
    ),
    # you can use a FileResponse if it's a file in disk with a path: https://www.starlette.io/responses/#fileresponse.
    # If it's a file-like object created in your path operation, in the next stable release of Starlette
    # (used internally by FastAPI) you will also be able to return it in a StreamingResponse.
    Route("/video", views.video, name="video"),
    Route("/videostream", views.video_stream, name="videostream"),
    Route("/videofile", views.video_file, name="videofile"),
]
