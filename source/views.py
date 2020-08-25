from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse

from source.templates import render
import source.openapi as api

"""
Views get data from primarily openapi, that has a jsonapi-interface with data and possibly links, meta and includes.
Views send data to templates in optimal structure via context
"""


async def index(request: Request):
    return render("index.html", {"request": request})


async def about(request: Request):
    return render("about.html", {"request": request})


async def welcome(request: Request):
    return render("welcome.html", {"request": request})


async def search(request: Request):
    context = {"request": request}
    context["user"] = request.session.get("user")
    resp = await api.list_resources(request.query_params)

    if request.query_params.get("fmt", "") == "json":
        return JSONResponse(resp)

    # If SAM-request. It only wants id-lists
    if "ids" in request.query_params.getlist("view"):
        return JSONResponse(resp)

    if resp.get("errors"):
        context["errors"] = resp.get("errors")
        return render("error.html", context)

    # if resp.get("meta") and resp["meta"].get("filters"):
    #     context["filters"] = resp["meta"].get("filters")

    # if resp.get("links") and resp["links"].get("prev"):
    #     context["prev"] = resp["links"].get("prev")

    # if resp.get("links") and resp["links"].get("next"):
    #     context["next"] = resp["links"].get("next")

    # context["result"] = resp["data"]

    context.update(resp)
    return render("search.html", context)


async def video(request: Request):
    # open does not support async
    # videofile = open("./statics/video/futurama.mp4", mode="rb")
    return FileResponse("./statics/video/futurama.mp4", media_type="video/mp4")


async def image(request: Request):
    # videofile = open("./statics/video/futurama.mp4", mode="rb")
    return FileResponse("./statics/images/logo.png", media_type="image/png")
