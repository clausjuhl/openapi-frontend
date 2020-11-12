from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.datastructures import QueryParams

import source.openapi as api
from source.templates import render
from source.resources.helpers import format_record, generate_url


async def resource(req: Request):
    context = {"request": req}
    context["user"] = req.session.get("user")

    collection = req.path_params["collection"]
    item = req.path_params["item"]

    if req.method == "GET":
        query_params = req.query_params
        resp = await api.get_resource(collection, item, query_params)

        if query_params.get("fmt", "") == "json":
            return JSONResponse(resp)

        if resp.get("errors"):
            context["errors"] = resp.get("errors")
            return render("error.html", context)

        # if "traverse" and refererpage is search or resource-page, traversal
        # is ALMOST always intended
        if req.session.get("traverse") and (
            "/search?" or "/resources/" in req.headers.get("referer", "")
        ):
            traverse = req.session.get("traverse")
            cur_ids = traverse.get("cur_ids")
            start = traverse.get("start")
            size = traverse.get("size")
            total = traverse.get("total")
            cur_counter = int

            if item in cur_ids:
                idx = cur_ids.index(item)
                cur_counter = start + idx + 1

                if idx == 0 and start > 0:
                    key = str(start - size)
                    batches = traverse["batches"]
                    prev_url = generate_url(key, traverse["cur_search"])

                    # check if list of prev_ids (start - size) is already in batches
                    if key not in batches:
                        api_resp = api.list_resources(QueryParams(prev_url))
                        batches[key] = [
                            int(d.get("id")) for d in api_resp.get("result")
                        ]
                    traverse["prev_ids"] = batches[key]
                    # traverse["prev_results"] = prev_url
                    context["prev"] = traverse["prev_ids"][-1]

                if idx > 0:
                    context["prev"] = cur_ids[idx - 1]

                if idx < len(cur_ids) - 1:
                    context["next"] = cur_ids[idx + 1]

                if idx == len(cur_ids) - 1 and (start + size < total):
                    key = str(start + size)
                    batches = traverse["batches"]
                    next_url = generate_url(key, traverse["cur_search"])

                    if key not in batches:
                        api_resp = api.list_resources(QueryParams(next_url))
                        batches[key] = [
                            int(d.get("id")) for d in api_resp.get("result")
                        ]
                    traverse["next_ids"] = batches[key]
                    # traverse["next_results"] = next_url
                    context["next"] = traverse["next_ids"][0]

            elif traverse.get("next_ids") and item == traverse["next_ids"][0]:
                # Else if id first from "next_ids", update session before rendering
                cur_counter = start + size + 1
                traverse["start"] = start + size

                # requested item is the first from the next batch of results
                context["prev"] = traverse["cur_ids"][-1]
                if len(traverse["next_ids"]) > 1:
                    context["next"] = traverse["next_ids"][1]

                # move id-lists backward
                traverse["prev_ids"] = traverse["cur_ids"]
                traverse["cur_ids"] = traverse["next_ids"]
                traverse.pop("next_ids", None)

            elif traverse.get("prev_ids") and item == traverse["prev_ids"][-1]:
                cur_counter = start
                traverse["start"] = start - size

                # requested item is the last from the previous batch of results
                context["next"] = traverse["cur_ids"][0]
                if len(traverse["prev_ids"]) > 1:
                    context["prev"] = traverse["prev_ids"][-2]

                # move id-lists forward and remove prev_ids
                traverse["next_ids"] = traverse["cur_ids"]
                traverse["cur_ids"] = traverse["prev_ids"]
                traverse.pop("prev_ids", None)

            # If traversal, set these values no matter what
            context["current_search"] = traverse.get("cur_search")
            context["total"] = traverse.get("total")
            context["cur_counter"] = cur_counter

        # if "traverse" and refererpage is search or resource-page, traversal
        # is ALMOST always intended
        # if req.session.get("traverse") and (
        #     "/search?" or "/resources/" in req.headers.get("referer", "")
        # ):
        #     traverse = req.session.get("traverse")
        #     cur_ids = traverse.get("cur_ids")
        #     start = traverse.get("start")
        #     size = traverse.get("size")
        #     total = traverse.get("total")
        #     cur_counter = None

        #     if item in cur_ids:
        #         idx = cur_ids.index(item)
        #         cur_counter = start + idx + 1

        #         # if item is the first in the current batch AND
        #         # there is a link to a previous resultset
        #         # if idx == 0 and traverse.get("prev_results"):
        #         if idx == 0 and start > 0:
        #             key = str(start - size)
        #             batches = traverse["batches"]
        #             # check if list of prev_ids (start - size) is already in batches
        #             if key in batches:
        #                 traverse["prev_ids"] = batches[key]
        #             elif traverse.get("prev_results"):
        #                 # fetch prev results and update session
        #                 api_resp = api.list_resources(
        #                     QueryParams(traverse["prev_results"])
        #                 )
        #                 traverse["prev_ids"] = [
        #                     int(d.get("id")) for d in api_resp.get("result")
        #                 ]
        #                 batches[key] = traverse["prev_ids"]
        #                 # put "prev"-link into "past_results"

        #                 traverse["past_results"] = api_resp.get("prev", None)

        #             # use last id from prev_ids as prev
        #             context["prev"] = traverse["prev_ids"][-1]

        #         if idx > 0:
        #             context["prev"] = cur_ids[idx - 1]

        #         if idx < len(cur_ids) - 1:
        #             context["next"] = cur_ids[idx + 1]

        #         # if idx == len(cur_ids) - 1 and traverse.get("next_results"):
        #         if idx == len(cur_ids) - 1 and (start + size < total):
        #             # fetch next results and update session
        #             key = str(start + size)
        #             batches = traverse["batches"]
        #             if key in batches:
        #                 traverse["next_ids"] = batches[key]
        #             elif traverse.get("next_results"):
        #                 api_resp = api.list_resources(
        #                     QueryParams(traverse["next_results"])
        #                 )
        #                 traverse["next_ids"] = [
        #                     int(d.get("id")) for d in api_resp.get("result")
        #                 ]
        #                 batches[key] = traverse["next_ids"]
        #                 traverse["future_results"] = api_resp.get("next", None)

        #             # use first id from next_ids as next
        #             context["next"] = traverse["next_ids"][0]

        #     elif traverse.get("next_ids") and item == traverse["next_ids"][0]:
        #         # Else if id first from "next_ids", update session before rendering
        #         cur_counter = start + size + 1
        #         traverse["start"] = start + size

        #         # requested item is the first from the next batch of results
        #         context["prev"] = traverse["cur_ids"][-1]
        #         if len(traverse["next_ids"]) > 1:
        #             context["next"] = traverse["next_ids"][1]

        #         # move id-lists backward and remove next_ids
        #         traverse["prev_ids"] = traverse["cur_ids"]
        #         traverse["cur_ids"] = traverse["next_ids"]
        #         # traverse.pop("next_ids", None)
        #         # traverse.pop("prev_ids", None)
        #         # move results-urls backwards and remove future_results
        #         traverse["prev_results"] = traverse["cur_results"]
        #         traverse["cur_results"] = traverse["next_results"]
        #         traverse["next_results"] = traverse.get("future_results")
        #         # traverse.pop("future_results", None)
        #         # traverse.pop("next_results", None)

        #     elif traverse.get("prev_ids") and item == traverse["prev_ids"][-1]:
        #         cur_counter = start
        #         traverse["start"] = start - size

        #         # requested item is the last from the previous batch of results
        #         context["next"] = traverse["cur_ids"][0]
        #         if len(traverse["prev_ids"]) > 1:
        #             context["prev"] = traverse["prev_ids"][-2]

        #         # move id-lists forward and remove prev_ids
        #         traverse["next_ids"] = traverse["cur_ids"]
        #         traverse["cur_ids"] = traverse["prev_ids"]
        #         # traverse.pop("prev_ids")
        #         # traverse.pop("next_ids")
        #         # move results-urls forward and remove prev_results
        #         traverse["next_results"] = traverse["cur_results"]
        #         traverse["cur_results"] = traverse["prev_results"]
        #         traverse["prev_results"] = traverse.get("past_results")
        #         # traverse.pop("past_results", None)
        #         # traverse.pop("prev_results", None)

        #     # If traversal, set these values no matter what
        #     context["current_search"] = traverse.get("cur_results")
        #     context["total"] = traverse.get("total")
        #     context["cur_counter"] = cur_counter

        context["resource"] = format_record(resp.get("data"))

        if collection and collection in ["creators", "collectors"]:
            collection = resource.get("domain")
        context["collection"] = collection

        return render("resource.html", context)
