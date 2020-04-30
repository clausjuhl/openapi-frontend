from starlette.routing import Route
from source.auth import views


routes = [
    Route("/login", endpoint=views.login, name="login"),
    Route("/logout", endpoint=views.logout, name="logout"),
    Route("/callback", endpoint=views.callback, name="callback"),
]
