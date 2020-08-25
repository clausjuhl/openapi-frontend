import json

import boto3

from source import settings
from source.configuration import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION_NAME,
    AWS_CLOUDSEARCH_ENDPOINT,
)


class SearchHandler:
    def __init__(self):
        self.filters = settings.QUERY_PARAMS
        self.search_engine = boto3.client(
            "cloudsearchdomain",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION_NAME,
            endpoint_url=AWS_CLOUDSEARCH_ENDPOINT,
        )

    def list_facets(self):
        # lists all facet-values from the searchengine
        facet_options = {
            "availability": {},
            "usability": {},
            "content_types": {"size": 100},
            "subjects": {"size": 100},
        }

        key_args = {}
        key_args["facet"] = json.dumps(facet_options)
        key_args["returnFields"] = "_no_fields"
        key_args["size"] = 1
        key_args["queryParser"] = "structured"
        key_args["query"] = "matchall"

        resp = self.search_engine.search(**key_args)
        return resp.get("facets")

    def list_collection_facets(self, collection_id):
        # lists all series and collection_tags of a given collection
        facet_options = {
            "collection_tags": {"sort": "count", "size": 7000},
            "series": {"sort": "count", "size": 2000},
        }

        key_args = {}
        key_args["query"] = "matchall"
        key_args["facet"] = json.dumps(facet_options)
        key_args["returnFields"] = "_no_fields"
        key_args["size"] = 1
        key_args["queryParser"] = "structured"
        key_args["query"] = "matchall"
        key_args["filterQuery"] = "collection:'" + str(collection_id) + "'"

        resp = self.search_engine.search(**key_args)
        return resp.get("facets")

    def search_records(self, query_params):
        # https://docs.aws.amazon.com/cloudsearch/latest/developerguide/search-api.html#structured-search-syntax
        # https://docs.aws.amazon.com/cloudsearch/latest/developerguide/searching-compound-queries.html

        # Kwargs to send to all bobo3-cloudsearch-calls.
        key_args = {}
        key_args["queryParser"] = "structured"
        key_args["queryOptions"] = json.dumps(
            {"fields": ["label^4", "summary^2", "description"]}
        )

        # Variables
        date_from = query_params.get("date_from")
        date_to = query_params.get("date_to")
        q = query_params.get("q")

        ####################
        # SORT + DIRECTION #
        ####################
        # default values
        sort = query_params.get("sort", "date_from")
        direction = query_params.get("direction", "asc")
        # Override if no explicit sort is selected.
        if not query_params.get("sort"):
            # If fulltext-search, then rank by relevance
            if q:
                sort = "_score"
                direction = "desc"
            # If date_to is set, override relevance-sorting
            if date_to:
                sort = "date_to"
                direction = "desc"
            # If date_from is set, overrides relevance and date_to
            if date_from:
                sort = "date_from"
                direction = "asc"

        key_args["sort"] = " ".join([sort, direction])  # aws-convention

        ###########
        # Q-PARAM #
        ###########
        # Fulltext query - wrap value in single-quotes or if empty use
        # "matchall" to enable filtered searches without a q-param
        if q and q.strip():
            # tokens = q.strip().split(' ')
            tokens = q.split(" ")
            if tokens:
                strs = []
                phrase = None
                phrase_strs = []

                for s in tokens:
                    # no need to bother
                    if len(s) < 2:
                        continue

                    # If single-word phrase
                    if not phrase and s.startswith('"') and s.endswith('"'):
                        strs.append("'" + s[1:-1] + "'")

                    # Elif single-word negative phrase
                    elif not phrase and s.startswith('-"') and s.endswith('"'):
                        strs.append("'" + s[2:-1] + "'")

                    # Elif a phrase is active, add token if not the ending
                    elif phrase and not (s.endswith('"') or s.startswith('"')):
                        phrase_strs.append(s)

                    elif s.startswith('-"') and not phrase:
                        # start a new phrase and append string
                        phrase = "negated"
                        # s = re.sub('*', '', s)
                        phrase_strs.append(s[2:])

                    elif s.startswith('"') and not phrase:
                        # start a new phrase and append string
                        phrase = "positive"
                        phrase_strs.append(s[1:])

                    elif s.endswith('"') and phrase:
                        # append string and close phrase
                        phrase_strs.append(s[:-1])
                        if phrase == "positive":
                            strs.append(
                                "(phrase '" + " ".join(phrase_strs) + "')"
                            )
                        else:
                            strs.append(
                                "(not (phrase '"
                                + " ".join(phrase_strs)
                                + "'))"
                            )
                        # Ready for new phrase
                        phrase = None
                        phrase_strs = []

                    elif s.startswith("-"):
                        if s.endswith("*"):
                            strs.append("(not (prefix '" + s[:-1] + "'))")
                        else:
                            strs.append("(not '" + s[1:] + "')")

                    elif s.endswith("*"):
                        strs.append("(prefix '" + s[:-1] + "')")

                    else:
                        strs.append("'" + s + "'")

            if len(tokens) > 1:
                key_args["query"] = "(and " + " ".join(strs) + ")"
            else:
                # key_args['query'] = "'" + strs[0] + "'"
                key_args["query"] = strs[0]

        else:
            key_args["query"] = "matchall"

        ############
        # FQ-PARAM #
        ############
        filters_to_query = (
            []
        )  # list of query-filters used for key_arg: "filterQuery"
        filters_to_output = []  # list of filters used for gui-template

        # Build "filterQuery"-arg
        for key in query_params.keys():

            # remove any negation
            stripped_key = key[1:] if key.startswith("-") else key
            filter_type = self.filters[stripped_key].get("type")

            # q-param already processed
            if stripped_key == "q":
                continue

            # Leave out non-searchfilters from filterQuery, eg. "size", "direction", "start"
            if not self.filters[stripped_key].get("search_filter"):
                continue

            # Go back to using the full key-label before iterating query
            for value in query_params.getlist(key):

                if filter_type == "object":
                    filter_str = ":".join([stripped_key, "'" + value + "'"])
                    # if negation, update filter_str
                    if stripped_key != key:
                        filter_str = "(not " + filter_str + ")"
                    filters_to_query.append(filter_str)
                    filters_to_output.append(
                        {
                            "key": stripped_key,
                            "value": value,
                            "negated": stripped_key != key,
                            "unresolved": True,
                        }
                    )

                elif filter_type in ["string", "integer"]:
                    filter_str = ":".join([stripped_key, "'" + value + "'"])
                    # if negation, update filter_str
                    if stripped_key != key:
                        filter_str = "(not " + filter_str + ")"
                    filters_to_query.append(filter_str)
                    filters_to_output.append(
                        {
                            "key": stripped_key,
                            "value": value,
                            "negated": stripped_key != key,
                        }
                    )

                elif key == "date_from":
                    filters_to_query.append("date_from:[" + value + ",}")
                    filters_to_output.append({"key": key, "value": value})

                elif key == "date_to":
                    filters_to_query.append("date_to:{," + value + "]")
                    filters_to_output.append({"key": key, "value": value})

        if filters_to_query:
            key_args["filterQuery"] = (
                "(and " + " ".join(filters_to_query) + ")"
            )

        ###############
        # SAM-request #
        ###############
        if "ids" in query_params.getlist("view"):
            # Additional request key_args
            key_args["returnFields"] = "_no_fields"
            key_args["size"] = query_params.get("size", 1000, int)
            if query_params.get("cursor"):
                key_args["cursor"] = query_params.get("cursor")
            else:
                key_args["cursor"] = "initial"

            # Make request to Cloudsearch
            api_response = self.search_engine.search(**key_args)

            # Build simple response
            out = {}
            out["status_code"] = 0  # Needed for SAM
            out["result"] = []
            if key_args.get("size") + api_response["hits"].get(
                "start"
            ) < api_response["hits"].get("found"):
                out["next_cursor"] = api_response["hits"].get("cursor")
            for hit in api_response["hits"]["hit"]:
                out["result"].append(hit["id"])
            return out

        ####################
        # Standard-request #
        ####################
        else:
            # Additional request key_args
            key_args["facet"] = json.dumps(
                {
                    "availability": {},
                    "usability": {},
                    "content_types": {"size": 100},
                    "subjects": {"size": 100},
                    "collection": {"size": 40},
                }
            )
            key_args[
                "returnFields"
            ] = "label,summary,collection,series,content_types,thumbnail,portrait,collectors_label,date_from,date_to,created_at,availability,updated_at"
            key_args["start"] = query_params.get("start", 0, int)
            key_args["size"] = query_params.get("size", 20, int)

            # Make request to Cloudsearch
            api_response = self.search_engine.search(**key_args)

            # Build response
            out = {}
            out["sort"] = sort
            out["direction"] = direction
            out["size"] = key_args["size"]
            out["date_from"] = date_from
            out["date_to"] = date_to
            out["_query_string"] = key_args["query"]  # processed query-string
            out["total"] = api_response["hits"]["found"]
            out["start"] = api_response["hits"]["start"]
            out["facets"] = api_response["facets"]
            out["query"] = q or None  # original query-string

            # Parse hits from Cloudsearch
            records = []
            for hit in api_response["hits"]["hit"]:
                item = {}
                item["id"] = hit["id"]

                label = hit["fields"].get("label")
                item["label"] = label[0] if label else None

                summary = hit["fields"].get("summary")
                item["summary"] = summary[0] if summary else None

                item["content_types"] = hit["fields"].get("content_types")

                collection_id = hit["fields"].get("collection")
                item["collection_id"] = (
                    collection_id[0] if collection_id else None
                )

                collectors_label = hit["fields"].get("collectors_label")
                item["collectors_label"] = (
                    collectors_label[0] if collectors_label else None
                )

                item["series"] = hit["fields"].get("series")

                thumbnail = hit["fields"].get("thumbnail")
                item["thumbnail"] = thumbnail[0] if thumbnail else None

                portrait = hit["fields"].get("portrait")
                item["portrait"] = portrait[0] if portrait else None

                availability = hit["fields"].get("availability")
                item["availability"] = (
                    availability[0] if availability else None
                )

                created_at = hit["fields"].get("created_at")
                item["created_at"] = created_at[0] if created_at else None

                updated_at = hit["fields"].get("updated_at")
                item["updated_at"] = updated_at[0] if updated_at else None

                date_from = hit["fields"].get("date_from")
                item["date_from"] = date_from[0] if date_from else None

                date_to = hit["fields"].get("date_to")
                item["date_to"] = date_to[0] if date_to else None

                records.append(item)
            out["result"] = records

            # Filters for gui-processing
            out["filters"] = filters_to_output or None

            return out
