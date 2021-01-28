# import json
# from datetime import datetime
from typing import Dict

from source import tables as tb
from source.database import database

# create or update user
# async def upsert_login_user(user_data: Dict) -> Dict:
#     query = tables.users.select("openid").where(
#         tables.users.c.openid == user_data["sub"]
#     )
#     user = await database.fetch_one(query)

#     if user is None:
#         query = tables.users.insert()
#         values = {
#             "openid": user_data["sub"],
#             "name": user_data["name"],
#             "email": user_data["email"],
#             "email_verified": user_data["email_verified"],
#         }
#         await database.execute(query, values=values)
#     else:
#         query = tables.users.update().where(
#             tables.users.c.openid == user["openid"]
#         )
#         values = {
#             "email": user_data["email"],
#             "email_verified": user_data["email_verified"],
#         }
#         await database.execute(query, values=values)

#     # fetch created user
#     query = tables.users.select().where(
#         tables.users.c.openid == user_data["sub"]
#     )
#     return await database.fetch_one(query)


async def update_user(openid: str, update_values: Dict):
    query = tb.users.update().where(tb.users.c.openid == openid)
    await database.execute(query, values=update_values)

    # fetch created user
    query = tb.users.select().where(tb.users.c.openid == openid)
    return await database.fetch_one(query)


async def get_user(openid: str) -> Dict:
    query = tb.users.select().where(tb.users.c.openid == openid)
    return await database.fetch_one(query)
