import json
from typing import Dict, List

from starlette.datastructures import QueryParams

from source import settings, http

"""
Checks urls, permissions, requests, responses
All in accordance with a openapi-description and the clientsettings
E.g. openapi defines the requestparams and responsemodels; clientsettings
define default query-params or "filter"

RETURNS:
    "errors": List[{"code", "msg", "id" (optional item-id)}]
        OR
    "data": Dict or List[Dict],
"""


# Adds item-id to error. Used by bookmarks, searches,
async def _error(code: int, detail: str, item: int = None) -> Dict:
    error = {"code": code, "detail": detail}
    if item:
        error["id"] = item
    return {"errors": [error]}


async def get_resource(collection: str, item: int, params: QueryParams = None):
    if collection not in settings.RESOURCE_ENDPOINTS:
        return _error(404, "NOT FOUND. No such collection: " + collection)

    host = settings.RESOURCE_HOST
    resource = settings.RESOURCE_ENDPOINTS[collection]

    return await http.get_request(f"{host}/{resource}/{item}", params)


# 'batch_records' from ClientInterface reformatted
# def multi_get_records(id_list: List):

#     data = {"view": "record", "oasid": json.dumps(id_list)}
#     r = self._api_request(path="resolve_records_v2", method="post", data=data)

#     if r.get("status_code") == 0:
#         return r.get("result")

#     else:
#         return {
#             "errors": [
#                 {"code": r.get("status_code"), "msg": r.get("status_msg")}
#             ]
#         }


# 'resolve_params'
# def get_entity_labels(self, resource_list):
#     # resource_list: [('collection', '4'), ('availability', '2')]
#     r = self._api_request("resolve_params", params=resource_list)

#     if r.get("status_code") == 0:
#         output = []
#         for key, value in r.get("resolved_params").items():
#             for k, v in value.items():
#                 d = {"resource": key, "id": k, "label": v.get("display_label")}
#                 output.append(d)
#         return {"result": output}
#     else:
#         return {
#             "errors": [
#                 {"code": r.get("status_code"), "msg": r.get("status_msg")}
#             ]
#         }
