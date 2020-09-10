from starlette.requests import Request

from starlette.datastructures import QueryParams

import source.openapi as api
from source.templates import render


async def resource(req: Request):
    context = {"request": req}
    context["user"] = req.session.get("user")

    collection = req.path_params["collection"]
    item = req.path_params["item"]

    if req.method == "GET":
        query_params = req.query_params
        resp = await api.get_resource(collection, item, query_params)

        if resp.get("errors"):
            context["errors"] = resp.get("errors")
            return render("error.html", context)

        # if "traverse" and referer is search or resource-page, traversal
        # is almost always intended
        if req.session.get("traverse") and (
            "/search?" or "/resources/" in req.headers.get("referer", "")
        ):
            traverse = req.session.get("traverse")
            cur_ids = traverse.get("cur_ids")

            if item in cur_ids:
                idx = cur_ids.index(item)
                if idx == 0 and traverse.get("prev_results"):
                    # fetch prev results and update session
                    api_resp = api.list_resources(
                        QueryParams(traverse["prev_results"])
                    )
                    traverse["prev_ids"] = [
                        int(d.get("id")) for d in api_resp.get("result")
                    ]
                    traverse["past_results"] = api_resp.get("previous")
                    # use last id from prev_ids as prev_item
                    context["prev_item"] = traverse["prev_ids"][-1]

                if idx > 0:
                    context["prev_item"] = cur_ids[idx - 1]

                if idx < len(cur_ids) - 1:
                    context["next_item"] = cur_ids[idx + 1]

                if idx == len(cur_ids) - 1 and traverse.get("next_results"):
                    # fetch next results and update session
                    api_resp = api.list_resources(
                        QueryParams(traverse["next_results"])
                    )
                    traverse["next_ids"] = [
                        int(d.get("id")) for d in api_resp.get("result")
                    ]
                    traverse["future_results"] = api_resp.get("next")
                    # use first id from next_ids as next_item
                    context["next_item"] = traverse["next_ids"][0]

            elif traverse.get("next_ids") and item == traverse["next_ids"][0]:
                # requested item is the first from the next batch of results
                context["next_item"] = traverse["next_ids"][1]
                context["prev_item"] = traverse["cur_ids"][-1]
                # move id-lists backward and remove next_ids
                traverse["prev_ids"] = traverse["cur_ids"]
                traverse["cur_ids"] = traverse["next_ids"]
                traverse.pop("next_ids")
                # move results-urls backwards and remove future_results
                traverse["prev_results"] = traverse["cur_results"]
                traverse["cur_results"] = traverse["next_results"]
                traverse["next_results"] = traverse["future_results"]
                traverse.pop("future_results")

            elif traverse.get("prev_ids") and item == traverse["prev_ids"][-1]:
                # requested item is the last from the previous batch of results
                context["next_item"] = traverse["cur_ids"][0]
                context["prev_item"] = traverse["prev_ids"][-2]
                # move id-lists forward and remove prev_ids
                traverse["next_ids"] = traverse["cur_ids"]
                traverse["cur_ids"] = traverse["prev_ids"]
                traverse.pop("prev_ids")
                # move results-urls forward and remove prev_results
                traverse["next_results"] = traverse["cur_results"]
                traverse["cur_results"] = traverse["prev_results"]
                traverse["prev_results"] = traverse["past_results"]
                traverse.pop("past_results")

            context["current_search"] = traverse.get("cur_results")

        context["resource"] = resp.get("data")
        return render("resource.html", context)
