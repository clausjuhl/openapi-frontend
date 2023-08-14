from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from starlette.exceptions import HTTPException

from source.templates import render

# from source import queries
# from source import openapi as api
# from source.queries import update_user


async def profile(request: Request):
    if not request.session.get("user"):
        raise HTTPException(404)

    user = request.session["user"]
    context = {"request": request, "user": user}

    if request.method == "GET":
        if request.url.path.endswith(":edit"):
            return render("users/profile_editor.html", context)
        else:
            return render("users/profile.html", context)

    if request.method == "POST":
        form_values = await request.form()
        # form_errors = validate_input(model="user", values=dict(form_values))
        form_errors = False

        if form_errors:
            context["form_values"] = dict(form_values)
            context["form_errors"] = form_errors
            # render profile_editor with values and error-messages
            return render("profile_editor.html", context, status_code=400)

        # values = {"name": form_values.get("username")}
        # await queries.update_user(user["openid"], values=values)
        # else redirect to profile-page
        return RedirectResponse(url=request.url_for("profile"), status_code=303)


# async def profile_editor(request: Request):
#     user = request.session["user"]
#     if not user:
#         raise HTTPException(404)

#     context = {"request": request, "user": user}
#     render("users/profile_editor.html", context)


# INCLUDES ajax-stuff. Only enabled when js is working. Responds with JSONResponse
async def bookmarks(request: Request):
    user = request.session["user"]
    if not user:
        raise HTTPException(404)

    bookmarks = user.get("bookmarks") or []

    if request.method == "GET":
        context = {"request": request, "user": user}
        if bookmarks:
            context["bookmarks"] = bookmarks
            # fetch full records
            # context["bookmarks"] = await api.get_records(id_list=bookmarks)
        return render("users/bookmarks.html", context)

    if request.method == "POST":
        bookmark = await request.json()
        resource_id = bookmark.get("resource_id")

        if not resource_id:
            return JSONResponse({"error": "Manglende materialeID"})

        if resource_id in bookmarks:
            return JSONResponse({"error": "Materialet var allerede bogmærket"})

        # update db
        # bookmark = {"user_id": user["openid"], "resource_id": resource_id}
        # await queries.insert_bookmark(bookmark)

        # update session
        user["bookmarks"] = bookmarks.extend(resource_id)

        # generate response
        response = JSONResponse({"msg": "Bogmærke tilføjet"})
        response.set_cookie("user", user)
        return response


async def bookmark(request: Request):
    if not request.session.get("user"):
        raise HTTPException(404)

    resource_id = request.path_params.get("resource_id")
    user = request.session["user"]
    bookmarks = user.get("bookmarks") or []

    if request.method == "DELETE":

        if resource_id not in bookmarks:
            return JSONResponse({"error": "Materialet var ikke bogmærket"})

        # update db
        # bookmark = {"user_id": user["openid"], "resource_id": resource_id}
        # await queries.delete_bookmark(bookmark)

        # update session
        bookmarks.remove(resource_id)
        user["bookmarks"] = bookmarks

        # generate response
        response = JSONResponse({"msg": "Bogmærke fjernet"})
        response.set_cookie("user", user)
        return response


async def searches(request: Request):
    if not request.session.get("user"):
        raise HTTPException(404)

    user = request.session["user"]
    searches = user.get("searches", [])

    if request.method == "GET":
        context = {"request": request, "user": user}
        # searches = await queries.get_searches(user["openid"])
        if searches:
            context["searches"] = searches
        return render("users/searches.html", context)

    if request.method == "POST":
        search = await request.json()
        url = search.get("url")
        if not url:
            return JSONResponse({"error": "Manglende søgestreng"})

        if url in searches:
            return JSONResponse({"error": "Søgningen var allerede gemt"})

        # update db
        # search = {"user_id": user["openid"], "url": url, "description": search.get("description")}
        # await queries.insert_search(search)

        # update session
        user["searches"] = searches.extend(url)

        # generate response
        response = JSONResponse({"msg": "Søgning gemt"})
        response.set_cookie("user", user)
        return response
