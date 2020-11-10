from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse

from source.session import generate_session
from source.templates import render
import source.openapi as api

"""
Views get data from primarily openapi, that has a jsonapi-interface with data and possibly links, meta and includes.
Views send data to templates in optimal structure via context
"""


async def index(req: Request):
    return render("index.html", {"request": req})


async def about(req: Request):
    return render("about.html", {"request": req})


async def welcome(req: Request):
    return render("welcome.html", {"request": req})


async def search(req: Request):
    context = {"request": req}
    context["user"] = req.session.get("user")
    resp = api.list_resources(req.query_params)

    # If json-req
    if req.query_params.get("fmt", "") == "json":
        return JSONResponse(resp)

    # If SAM-req. It only wants json-encoded id-lists
    if "ids" in req.query_params.getlist("view"):
        return JSONResponse(resp)

    # If errors, show error-page
    if resp.get("errors"):
        context["errors"] = resp.get("errors")
        return render("error.html", context)

    # enables (and resets) traversal TODO: Remember to remove again
    req.session["traverse"] = {
        "cur_results": req.url.query,
        "cur_ids": [int(d.get("id")) for d in resp.get("result")],
        "total": resp.get("total"),
        # "size": resp.get("size"),
        "start": resp.get("start"),
        "next_results": resp.get("next"),
        "prev_results": resp.get("prev"),
    }

    context.update(resp)
    return render("search.html", context)


async def video(req: Request):
    # open does not support async
    # videofile = open("./statics/video/futurama.mp4", mode="rb")
    return FileResponse("./statics/video/futurama.mp4", media_type="video/mp4")


async def image(req: Request):
    return FileResponse(
        "./statics/images/logo_black.png", media_type="image/png"
    )


async def clear(req: Request):
    req.session.clear()
    return render("clear.html", {"request": req})
