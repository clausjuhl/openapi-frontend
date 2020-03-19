import json
from typing import Dict

from starlette.datastructures import URL, QueryParams

from source import settings, http


    # def _api_request(self, path, method="get", params=None, data=None):
    #     # Always returns a dict with 'status_code' plus 'result' or 'status_msg'
    #     if method == "get":
    #         r = requests.get("/".join([self.host, path]), params=params)
    #     else:
    #         r = requests.post("/".join([self.host, path]), data=data)

    #     try:
    #         r_to_dict = json.loads(r.content)
    #         return r_to_dict
    #     except ValueError as e:
    #         return {"status_code": 5, "status_msg": str(e)}

# async def error_response(code, message):


async def get_resource(collection: str, item: int):
    if collection not in settings.resource_endpoints:
        
    url = f"{settings.resource_host}/{settings.resource_endpoints[collection]}/{item}"
    res = http.get_request(url)
    if res.get("errors"):
        return res
    

    if r.get("status_code") == 0:
        return r.get("result")

    elif r.get("status_code") == 1:
        return {
            "errors": [
                {"code": 404, "msg": "Resourcen eksisterer ikke", "id": resource}
            ]
        }
    elif r.get("status_code") == 2:
        return {
            "errors": [{"code": 404, "msg": "Resourcen er slettet", "id": resource}]
        }
    else:
        return {
            "errors": [
                {
                    "code": r.get("status_code"),
                    "msg": r.get("status_msg"),
                    "id": resource,
                }
            ]
        }

# 'batch_records' from ClientInterface reformatted
def multi_get_records(self, id_list=None):
    if not id_list:
        return []

    data = {"view": "record", "oasid": json.dumps(id_list)}
    r = self._api_request(path="resolve_records_v2", method="post", data=data)

    if r.get("status_code") == 0:
        return r.get("result")

    else:
        return {
            "errors": [{"code": r.get("status_code"), "msg": r.get("status_msg")}]
        }

# 'resolve_params'
def get_entity_labels(self, resource_list):
    # resource_list: [('collection', '4'), ('availability', '2')]
    r = self._api_request("resolve_params", params=resource_list)

    if r.get("status_code") == 0:
        output = []
        for key, value in r.get("resolved_params").items():
            for k, v in value.items():
                d = {"resource": key, "id": k, "label": v.get("display_label")}
                output.append(d)
        return {"result": output}
    else:
        return {
            "errors": [{"code": r.get("status_code"), "msg": r.get("status_msg")}]
        }

async def _response(argument):
    return argument

async def get_resource(collection: str, item: str, query_params: QueryParams = None):