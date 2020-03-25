from starlette.requests import Request

# from starlette.exceptions import HTTPException

from source.templates import templates


async def index(request: Request):
    template = "index.jinja"
    context = {"request": request}
    return templates.TemplateResponse(template, context)


async def resource(request: Request):
    if request.method == "GET":
        template = "resource.jinja"
        context = {"request": request}
        structure = {
            "str": "value",
            "dict": {"key1": "val1", "key2": "val2"},
            "list": [
                {"idx0key1": "idx0val1"},
                ["idx1idx0", "idx1idx0"],
                "idx2",
            ],
        }
        context["structure"] = structure
        return templates.TemplateResponse(template, context)


# async def profile(req: Request):
#     """
#     Userhome
#     """
#     context = dict()
#     username = uestpath_params["username"]

#     if req.method == "GET":
#         status_code = 200

#     if req.method == "POST":
#         form_values = await req.form()
#         validated_data, form_errors = validate_or_error(form_values)
#         if not form_errors:
#             # await database.execute(query, values=insert_data)
#             return RedirectResponse(url=req.url, status_code=303)
#         status_code = 400
#     else:
#         status_code = 200

#     template = "profile.jinja"
#     context = {"request": req, "form_errors": form_errors}

#     return templates.TemplateResponse(
#         template, context, status_code=status_code
#     )


# async def error(req: Request):
#     """
#     An example error. Switch the debug setting to see tracebacks or 500 page.
#     """
#     raise RuntimeError("Oh no")


# async def not_found(req: Request):
#     """
#     Return an HTTP 404 page.
#     """
#     template = "404.jinja"
#     context = {"request": req}
#     return templates.TemplateResponse(template, context, status_code=404)


# async def error(request: Request):
#     """
#     Return an HTTP Error page.
#     """
#     template = "error.jinja"
#     context = {"request": request}
#     if request.app.debug:
#         raise HTTPException(code)
#     return templates.TemplateResponse(template, context, status_code=code)
