from starlette.requests import Request

import source.openapi as api
from source.templates import render


async def resource(request: Request):
    context = {"request": request}
    context["user"] = request.session.get("user")

    collection = request.path_params["collection"]
    item = request.path_params["item"]

    if request.method == "GET":
        query_params = request.query_params
        resp = await api.get_resource(collection, item, query_params)

        if resp.get("errors"):
            context["errors"] = resp.get("errors")
            return render("error.html", context)

        context["resource"] = resp.get("data")
        return render("resource.html", context)
