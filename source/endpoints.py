from source.templates import templates


async def homepage(request):
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)


# async def profile(request):
#     """
#     Userhome
#     """
#     context = dict()
#     username = request.path_params["username"]

#     if request.method == "GET":
#         status_code = 200

#     if request.method == "POST":
#         form_values = await request.form()
#         validated_data, form_errors = validate_or_error(form_values)
#         if not form_errors:
#             # await database.execute(query, values=insert_data)
#             return RedirectResponse(url=request.url, status_code=303)
#         status_code = 400
#     else:
#         status_code = 200

#     template = "profile.html"
#     context = {"request": request, "form_errors": form_errors}

#     return templates.TemplateResponse(
#         template, context, status_code=status_code
#     )


async def resource(request):
    """

    """
    if request.method == "GET":
        template = "resource.html"
        context = {"request": request}
        return templates.TemplateResponse(template, context)


async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)
