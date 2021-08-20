from starlette.routing import Route, Mount

from source import views
from source.staticfiles import statics
# from source.auth.routes import routes as auth_routes
# from source.users.routes import routes as users_routes
from source.resources.routes import routes as resources_routes

routes = [
    Route("/", views.index, name="home"),
    Route("/about", views.about, name="about"),
    Route("/search", views.search, name="search"),
    Route("/welcome", views.welcome, name="welcome"),
    # Route("/video", views.video, name="video"),
    Route("/image", views.image, name="image"),
    Route("/clear-session", views.clear, name="clear-session"),
    Mount("/resources", routes=resources_routes),
    # Mount("/users", routes=users_routes),
    # Mount("/auth", routes=auth_routes),
    Mount("/static", statics, name="static"),
]
