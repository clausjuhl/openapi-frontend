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
    Route(
        "/me/bookmarks/{resource_id}",
        views.bookmark,
        name="bookmark",
        methods=["DELETE"],
    ),
    Route(
        "/me/searches",
        views.searches,
        name="searches",
        methods=["GET", "POST"],
    ),
    # Route(
    #     "/me/searches/{search_id}",
    #     views.search,
    #     name="search",
    #     methods=["PUT", "DELETE"],
    # ),
]
