from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from starlette.exceptions import HTTPException

from source.templates import render
from source import queries
from source import openapi as api
from source.queries import update_user


async def profile(request: Request):
    if not request.session.get("user"):
        raise HTTPException(404)

    user = request.session["user"]
    context = {"request": request, "user": user}

    if request.method == "GET":
        if request.url.path.endswith("edit"):
            return render("profile_editor.html", context)
        else:
            return render("profile.html", context)

    if request.method == "POST":
        form_values = await request.form()
        # form_errors = validate_input(model="user", values=dict(form_values))
        form_errors = False

        if form_errors:
            context["form_values"] = dict(form_values)
            context["form_errors"] = form_errors
            # render profile_editor with values and error-messages
            return render("profile_editor.html", context, status_code=400)

        values = {"name": form_values.get("name")}
        # await queries.update_user(user["openid"], values=values)
        # else redirect to profile-page
        return RedirectResponse(
            url=request.url_for("users:profile"), status_code=303
        )


# INCLUDES ajax-stuff. Only enabled when js is working. Responds with JSONResponse
async def bookmarks(request: Request):
    if not request.session.get("user"):
        raise HTTPException(404)

    user = request.session["user"]
    context = {"request": request, "user": user}
    bookmarks = user.get("bookmarks", [])

    if request.method == "GET":
        if bookmarks:
            context["bookmarks"] = await api.get_records(id_list=bookmarks)
        return render("bookmarks.html", context)

    if request.method == "POST":
        data = request.json()
        resource_id = data.get("resource_id")

        if not resource_id:
            return JSONResponse({"error": "Manglende materialeID"})

        if resource_id in user.get("bookmarks", []):
            return JSONResponse({"error": "Materialet var bogmærket"})

        # update db
        # bookmark = {"user_id": user["openid"], "resource_id": resource_id}
        # await queries.create_bookmark(bookmark)

        # update session
        bookmarks.append(resource_id)
        user["bookmarks"] = bookmarks

        # generate response
        response = JSONResponse({"msg": "Bogmærke tilføjet"})
        response.set_cookie("user", user)
        await response


async def searches(request: Request):
    if not request.session.get("user"):
        raise HTTPException(404)

    user = request.session["user"]
    context = {"request": request, "user": user}

    if request.method == "GET":
        if user.get("searches"):
            context["searches"] = await queries.get_searches(user["openid"])
        return render("searches.html", context)
