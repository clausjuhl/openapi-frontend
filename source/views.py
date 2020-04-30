from starlette.requests import Request
from starlette.responses import FileResponse

from source.templates import render


async def index(request: Request):
    return render("index.html", {"request": request})


async def about(request: Request):
    return render("about.html", {"request": request})


async def welcome(request: Request):
    return render("welcome.html", {"request": request})


async def video(request: Request):
    # open does not support async
    # videofile = open("./statics/video/futurama.mp4", mode="rb")
    return FileResponse("./statics/video/futurama.mp4", media_type="video/mp4")


async def image(request: Request):
    # videofile = open("./statics/video/futurama.mp4", mode="rb")
    return FileResponse("./statics/images/logo.png", media_type="image/png")
