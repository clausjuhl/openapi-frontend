# import json
from typing import Dict, List

from urllib.parse import urlencode

from starlette.datastructures import QueryParams
from source import settings, http, searchInterface

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
def _error(code: int, detail: str, item: int = None) -> Dict:
    error = {"code": code, "detail": detail}
    if item:
        error["id"] = item
    return {"errors": [error]}


async def get_resource(collection: str, item: int, params: QueryParams = None):
    if collection not in settings.RESOURCE_ENDPOINTS:
        return _error(404, "NOT FOUND. No such collection: " + collection)

    host = settings.RESOURCE_HOST
    resource = settings.RESOURCE_ENDPOINTS[collection]

    resp = await http.get_request(f"{host}/{resource}/{item}", params)
    if resp.get("errors"):
        return resp
    return {"data": resp.get("result")}


def get_entity_labels(resource_list: List):
    # resource_list: [('collection', '4'), ('availability', '2')]
    host = settings.RESOURCE_HOST
    resp = http.get_request_sync(f"{host}/resolve_params", resource_list)

    if resp.get("errors"):
        return resp

    output = []
    for key, value in resp.get("resolved_params").items():
        for k, v in value.items():
            d = {"resource": key, "id": k, "label": v.get("display_label")}
            output.append(d)
    return {"data": output}


def list_resources(query_params: QueryParams = None):
    def _validate_query_params(query_params):
        errors = []
        stripped_keys = []

        for key in query_params:
            negated = key[0] == "-"
            stripped_key = key[1:] if negated else key

            if stripped_key not in settings.QUERY_PARAMS:
                errors.append({"param": key, "msg": "Invalid query-param"})
                continue  # no further tests needed

            if negated and not settings.QUERY_PARAMS[stripped_key].get(
                "negatable"
            ):
                errors.append({"param": key, "msg": "Param not negatable"})

            # Check if non-repeatable stripped_key already exists
            # eg. when using "-usability" and "usability"
            if stripped_key in stripped_keys and not settings.QUERY_PARAMS[
                stripped_key
            ].get("repeatable"):
                errors.append({"param": key, "msg": "Param not repeatable"})

            stripped_keys.append(stripped_key)

        # When all stripped_keys are iterated, test for series without collections.
        if "series" in stripped_keys and "collection" not in stripped_keys:
            errors.append(
                {
                    "param": "series",
                    "msg": "'Series'-key requires a 'collection'-key",
                }
            )

        return {"errors": errors}

    def _urlencode(params=None, remove=None, insert=None):

        temp_params = params[:] if params else []
        if insert:
            temp_params.append(insert)
        if remove and temp_params and (remove in temp_params):
            temp_params.remove(remove)
        return urlencode(temp_params)

    def _generate_filters(filters, params):
        # Adds links and creator-bools to filters
        out = []

        for f in filters:
            el = {}
            key = f.get("key")
            value = f.get("value")
            negated = f.get("negated")

            # get label if unresolved
            if f.get("unresolved"):
                r = get_entity_labels([(key, value)])
                if not r.get("errors"):
                    el["label"] = r["data"][0].get("label")

            # View-link
            # 'label' indicates an id-based filter which can be viewed
            if el.get("label"):
                if key == "collection":
                    el["view_link"] = "/".join(["collections", value])
                else:
                    el["view_link"] = "/".join([key, value])

            # Remove_link
            # If positive collection, also remove series
            # negative collection-params works like normal param
            if key == "collection" and not negated:
                new_params = [
                    (k, v)
                    for k, v in params
                    if k not in ["collection", "series", "start"]
                ]
                el["remove_link"] = urlencode(new_params)
            else:
                new_params = [(k, v) for k, v in params if k not in ["start"]]
                org_key = "-" + key if negated else key
                el["remove_link"] = _urlencode(
                    new_params, remove=(org_key, value)
                )

            # Inverse_link
            # If negated, replace with positive, vice versa
            # exception: if positive collection, remove series-param, as
            # it follows the collection
            if negated:
                new_params = [(k, v) for k, v in params if k not in ["start"]]
                el["invert_link"] = _urlencode(
                    new_params, remove=("-" + key, value), insert=(key, value)
                )
            else:
                if key == "collection":
                    new_params = [
                        (k, v)
                        for k, v in params
                        if k not in ["collection", "series", "start"]
                    ]
                    el["invert_link"] = _urlencode(
                        new_params, insert=("-" + key, value)
                    )
                else:
                    new_params = [
                        (k, v) for k, v in params if k not in ["start"]
                    ]
                    el["invert_link"] = _urlencode(
                        new_params,
                        insert=("-" + key, value),
                        remove=(key, value),
                    )
            # Creator and collector links and bools
            if key in ["people", "organisations"]:
                r = get_resource(key, int(value))
                if not r.get("errors"):
                    if r["data"].get("is_creative_creator"):
                        el["creator_link"] = "creators=" + value
                        el["creator"] = True
                    if r["data"].get("is_creator"):
                        el["creator_link"] = "collectors=" + value
                        el["collector"] = True

            el["negated"] = negated
            el["key"] = key
            el["value"] = value
            out.append(el)

        return out

    def _generate_facets(facets, params=None):
        # TODO: Does not work when excisting negative filter is set
        # and you click a positive facet: '-usability=4' is set, you click 'usability=2'
        result = {}
        params = [
            x for x in params if x[0] != "start"
        ]  # remove 'start'-param from facet-links
        for facet in facets:
            out = {}
            for b in facets[facet].get("buckets"):
                active = (facet, b.get("value"))  # tuple
                if params and (active in params):  # if
                    stripped_params = [x for x in params if x != active]
                    b["remove_link"] = urlencode(stripped_params)
                elif params:
                    b["add_link"] = urlencode(params + [active])
                else:
                    b["add_link"] = urlencode([active])
                out[b.get("value")] = b
            result[facet] = out
        return result

    def _generate_total_facets(aws_facets: Dict, params: List = None) -> Dict:
        # TODO: Does not work when excisting negative filter is set
        # and you click a positive facet: '-usability=4' is set, you click 'usability=2'

        def _recurse(
            facet_key: str,
            total_facet_values: List,
            active_facet_values: Dict,
            params: List = None,
        ) -> List:
            # total_facet_values is the "content"-key from each facet in settings.FACETS
            # active_facet_values is a dict of facet-values and facetinfo, e.g.
            # {"1": {"value": "1", "count": 63, "link": "add_or_remove_link_url"}}
            out = []
            for facet in total_facet_values:
                id_ = facet.get("id")
                label = facet.get("label")

                if id_ in active_facet_values:
                    current_tuple = (facet_key, id_)
                    el = {
                        "label": label,
                        "id": id_,
                        "count": active_facet_values[id_].get("count"),
                    }

                    if params and (
                        current_tuple in params
                    ):  # if the current tuple is in the params
                        stripped_params = [
                            x for x in params if x != current_tuple
                        ]
                        el["remove_link"] = urlencode(stripped_params)
                    elif params:
                        el["add_link"] = urlencode(params + [current_tuple])
                    else:
                        el["add_link"] = urlencode([current_tuple])

                    if facet.get("children"):
                        el["children"] = _recurse(
                            facet_key,
                            facet.get("children"),
                            active_facet_values,
                            params,
                        )
                    out.append(el)
            return out
            # return list of dicts with label, link and children

        # restructure aws-facets
        active_facets = {}
        for facet in aws_facets:
            active_facets[facet] = {
                b.get("value"): b for b in aws_facets[facet].get("buckets")
            }

        # remove 'start'-param from facet-links, retain all else
        params = [x for x in params if x[0] != "start"]
        result = {}

        for k, v in settings.FACETS.items():
            # label = facet.get("label")
            # recursively merge labels and links from total_facets and active_facets
            result[k] = _recurse(
                k, v.get("content"), active_facets.get(k), params
            )

        collection_tuples = [
            ("collection", key) for key in active_facets["collection"].keys()
        ]
        # result["collection_tuples"] = collection_tuples
        collection_labels = get_entity_labels(collection_tuples)
        # result["collection_labels"] = collection_labels

        result["collection"] = _recurse(
            "collection",
            collection_labels.get("data"),
            active_facets.get("collection"),
            params,
        )
        return result

    def _generate_views(params, view):
        output = []
        views = [
            {
                "label": "Listevisning",
                "value": "list",
                "icon": "fas fa-list",  # 'view_list'
            },
            {
                "label": "Galleri-visning",
                "value": "gallery",
                "icon": "fas fa-th",  # 'view_module'
            },
        ]

        if params:
            stripped_params = [(t[0], t[1]) for t in params if t[0] != "view"]
        else:
            stripped_params = []

        for option in views:
            current = {}
            current["label"] = option.get("label")
            current["icon"] = option.get("icon")
            if option.get("value") == view:
                current["selected"] = True
            else:
                current["link"] = urlencode(
                    stripped_params + [("view", option.get("value"))]
                )
            output.append(current)
        return output

    def _generate_sorts(params, sort, direction):
        sorts = [
            {
                "label": "Ældste dato først",
                "sort": "date_from",
                "direction": "asc",
            },
            {
                "label": "Nyeste dato først",
                "sort": "date_to",
                "direction": "desc",
            },
            {"label": "Relevans", "sort": "_score", "direction": "desc"},
        ]
        output = []

        if params:
            stripped_params = [
                (t[0], t[1])
                for t in params
                if t[0] not in ["sort", "direction", "start"]
            ]
        else:
            stripped_params = []

        for option in sorts:
            current = {}
            current["icon"] = option.get("icon")
            current["label"] = option.get("label")
            if (
                option.get("sort") == sort
                and option.get("direction") == direction
            ):
                current["selected"] = True
            else:
                current["link"] = urlencode(
                    stripped_params
                    + [
                        ("sort", option.get("sort")),
                        ("direction", option.get("direction")),
                    ]
                )
            output.append(current)
        return output

    def _generate_sizes(params, size):
        sizes = [20, 50, 100]
        output = []

        if params:
            stripped_params = [(t[0], t[1]) for t in params if t[0] != "size"]
        else:
            stripped_params = []

        for option in sizes:
            current = {}
            current["label"] = option
            if option == size:
                current["selected"] = True
            else:
                current["link"] = urlencode(
                    stripped_params + [("size", option)]
                )
            output.append(current)
        return output

    # Validate params
    if query_params:
        validated_request = _validate_query_params(query_params)
        if validated_request.get("errors"):
            return validated_request

    # Make api-call
    api_resp = searchInterface.search_records(query_params)

    # If api-error
    if api_resp.get("errors"):
        return api_resp

    # If SAM-request, no need for further processing
    # api_resp on request with "view=ids"-param includes three keys: status_code, result, next_cursor (optional)
    if "ids" in query_params.getlist("view"):
        return api_resp

    # Else process and convert response
    # api_resp on normal request includes: sort, direction, size, date_from,
    # date_to, _query_string, total, start, server_facets, filters, query, result,
    # view_list, sort_list, size_list, view, non_query_params
    resp = {}

    # convert multidict to list of tuples
    # params = [tup for tup in query_params.items(multi=True)]  # Flask-syntax
    params = [tup for tup in query_params.multi_items()]  # starlette-syntax
    # Keys used for generating searchviews and facets
    resp["params"] = params
    resp["query"] = api_resp.get("query", None)

    # If filters, generate links and possibly labels
    if api_resp.get("filters"):
        resp["filters"] = _generate_filters(api_resp["filters"], params)

    # if facets, generate links
    if api_resp.get("facets"):
        resp["facets"] = _generate_total_facets(api_resp["facets"], params)

    # 'non_query_params' is used to generate a remove_link for the q-param
    # on the zero-hits page
    if not api_resp.get("result") and api_resp.get("query"):
        other_params = [i for i in params if i != ("q", api_resp.get("query"))]
        resp["non_query_params"] = urlencode(other_params)

    # Pagination
    if api_resp.get("result"):
        total = api_resp["total"]
        start = api_resp["start"]
        size = api_resp["size"]
        rm_tup = ("start", str(start))
        if start > 0:
            resp["first"] = _urlencode(params, remove=rm_tup)
            resp["previous"] = _urlencode(
                params, remove=rm_tup, insert=("start", start - size)
            )

        if total <= 10000 and (start + size < total):
            last_start = total // size * size
            if last_start == total:
                last_start = total - size
            resp["last"] = _urlencode(
                params, remove=rm_tup, insert=("start", last_start)
            )

        if (start + size < total) and (start + size <= 10000):
            resp["next"] = _urlencode(
                params, remove=rm_tup, insert=("start", start + size)
            )

    # Proces size, sort, direction and view
    resp["size_list"] = _generate_sizes(params, api_resp["size"])
    resp["sort_list"] = _generate_sorts(
        params, api_resp["sort"], api_resp["direction"]
    )
    resp["view_list"] = _generate_views(
        params, query_params.get("view", "list")
    )
    resp["view"] = query_params.get("view", "list")
    resp["total"] = api_resp.get("total")
    resp["start"] = api_resp.get("start")
    resp["size"] = api_resp.get("size")
    resp["sort"] = api_resp.get("sort")
    resp["result"] = api_resp.get("result")
    # resp["api_response"] = api_resp.get("api_response")
    return resp

    #####################################################################
    # # ORIGINAL CODE - before copying searchInterface from aarhusarkivet
    #####################################################################

    # if params:
    #     url = f"{settings.SEARCH_URL}?{params}&fmt=json"
    # else:
    #     url = f"{settings.SEARCH_URL}?fmt=json"
    # resp = await http.get_request(url)

    # if resp.get("errors"):
    #     return resp

    # links, meta = {}, {}
    # if resp.get("previous"):
    #     links["prev"] = resp.get("previous")
    # if resp.get("next"):
    #     links["next"] = resp.get("next")
    # if resp.get("filters"):
    #     meta["filters"] = resp.get("filters")
    # return {"links": links, "meta": meta, "data": resp.get("result")}


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

