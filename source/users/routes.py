from starlette.routing import Route
from source.users import views


routes = [
    Route("/me", views.profile, name="profile", methods=["GET", "POST"]),
    Route("/me:edit", views.profile, name="profile_editor"),
    Route(
        "/me/bookmarks",
        views.bookmarks,
        name="bookmarks",
        methods=["GET", "POST"],
    ),
]
