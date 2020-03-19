from starlette.requests import Request
from starlette.exceptions import HTTPException

from source.templates import templates


async def index(req: Request):
    template = "index.html"
    context = {"request": req}
    return templates.TemplateResponse(template, context)


# async def profile(req: Request):
#     """
#     Userhome
#     """
#     context = dict()
#     username = req.path_params["username"]

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

#     template = "profile.html"
#     context = {"request": req, "form_errors": form_errors}

#     return templates.TemplateResponse(
#         template, context, status_code=status_code
#     )


async def resource(req: Request):
    """

    """
    if req.method == "GET":
        template = "resource.html"
        context = {"request": req}
        return templates.TemplateResponse(template, context)


# async def error(req: Request):
#     """
#     An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
#     """
#     raise RuntimeError("Oh no")


# async def not_found(req: Request):
#     """
#     Return an HTTP 404 page.
#     """
#     template = "404.html"
#     context = {"request": req}
#     return templates.TemplateResponse(template, context, status_code=404)


async def error(code: int, req: Request):
    """
    Return an HTTP Error page.
    """
    template = "error.html"
    context = {"request": req, "code": code}
    if req.app.debug:
        raise HTTPException(code)
    return templates.TemplateResponse(template, context, status_code=code)
