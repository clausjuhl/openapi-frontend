import json
from datetime import datetime

import httpx
from starlette.responses import RedirectResponse
from starlette.datastructures import URL

from source import settings, tables
from source.database import database

# from source.resources import database
from source.configuration import (
    AUTH0_CLIENT_ID,
    AUTH0_AUDIENCE,
    AUTH0_DOMAIN,
    AUTH0_CLIENT_SECRET,
    AUTH0_GRANT_TYPE,
)


async def login(request):
    if request.session.get("username"):
        url = request.url_for("profile")
        return RedirectResponse(url=url, status_code=303)

    params = {
        "redirect_uri": request.url_for("auth:callback"),
        "response_type": "code",
        "scope": "openid profile email",
        "client_id": AUTH0_CLIENT_ID,
        "audience": AUTH0_AUDIENCE,
    }
    url = URL(f"https://{AUTH0_DOMAIN}/authorize").include_query_params(
        **params
    )
    return RedirectResponse(url=url, status_code=303)


async def logout(request):
    request.session.clear()
    # logout of auth0
    query_params = {
        "returnTo": request.url_for("home"),
        "client_id": AUTH0_CLIENT_ID,
    }
    url = URL(f"https://{AUTH0_DOMAIN}/v2/logout").include_query_params(
        **query_params
    )
    return RedirectResponse(url)


async def callback(request):
    # get access token
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    data = {
        "code": request.query_params.get("code"),
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "redirect_uri": request.url_for("auth:callback"),
        "grant_type": AUTH0_GRANT_TYPE,
    }
    headers = {"content-type": "application/json"}
    # response = httpx.post(token_url, data=json.dumps(data), headers=headers)
    response = httpx.post(token_url, json=data, headers=headers)
    response.raise_for_status()  # check for errors
    data = response.json()

    # get user-data
    access_token = data["access_token"]
    user_url = f"https://{AUTH0_DOMAIN}/userinfo?access_token={access_token}"
    response = httpx.get(user_url)
    response.raise_for_status()
    data = response.json()

    # Upsert user
    query = tables.users.select("openid").where(
        tables.users.c.openid == data["sub"]
    )
    user = await database.fetch_one(query)
    new_user = False

    if user is None:
        query = tables.users.insert()
        values = {
            "openid": data["sub"],
            "name": data["name"],
            "email": data["email"],
            "email_verified": data["email_verified"],
        }
        await database.execute(query, values=values)
        new_user = True
    else:
        query = tables.users.update().where(
            tables.users.c.openid == user["openid"]
        )
        values = {
            "email": data["email"],
            "email_verified": data["email_verified"],
        }
        await database.execute(query, values=values)

    # fetch created user
    query = tables.users.select().where(tables.users.c.openid == data["sub"])
    # user = upsert_login_user(data)

    user = data
    request.session["user"] = user

    # query = tables.bookmarks.select(tables.bookmarks.c.resource_id).where(
    #     tables.bookmarks.c.user_id == user["pk"]
    # )
    # request.session["bookmarks"] = await database.fetch_many(query)

    if new_user:
        return RedirectResponse(request.url_for("welcome"), status_code=303)
    else:
        return RedirectResponse(request.url_for("profile"), status_code=303)
