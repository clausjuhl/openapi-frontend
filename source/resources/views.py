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
        response = await api.get_resource(collection, item, query_params)

        if response.get("errors"):
            context["errors"] = response.get("errors")
            return render("error.html", context)
        else:
            context["resource"] = response.get("data")
            return render("resource.html", context)
