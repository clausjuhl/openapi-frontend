from urllib.parse import urlencode

from source.settings import QUERY_PARAMS


def format_record(record):
    def _generate_hierarchical_structure(string_list):
        # Takes a list of strings with possible '/' as hierarchical seperators
        # Returns a dict-structure with 'label', 'path' and possibly 'children'-keys

        def addHierItem(key, hierStruct, hierList, parent):
            if parent != "":
                path = parent + "/" + key
            else:
                path = key

            hierItem = {"label": key, "path": path}

            childrenList = []
            children = hierStruct.get(key)
            for childKey in sorted(children):
                addHierItem(childKey, children, childrenList, path)

            if len(childrenList) > 0:
                hierItem["children"] = childrenList

            hierList.append(hierItem)

        hierList = []
        hierStruct = {}
        for item in sorted(string_list):
            splitList = item.split("/")

            curLevel = hierStruct
            for key in splitList:
                hierData = curLevel.get(key, {})
                curLevel[key] = hierData
                curLevel = hierData

        for key in sorted(hierStruct):
            addHierItem(key, hierStruct, hierList, "")

        return hierList

    result = {}
    for key, value in record.items():
        # First handle all specialcases
        # If 'series' then treat uniquely
        if key == "series":
            output = []
            currentLevel = []
            urlpath = {}
            collection = record.get("collection")

            if collection:
                urlpath["collection"] = collection.get("id")

            for idx in value.split("/"):
                currentLevel.append(idx)
                urlpath["series"] = "/".join(currentLevel)
                level = {}
                level["label"] = idx
                level["new_link"] = urlencode(urlpath)
                output.append(level)
            result[key] = output

        # If key is list of strings
        elif key in ["admin_tags"]:
            output = []
            for idx in value:
                item = {}
                item["label"] = idx
                item["new_link"] = urlencode({key: _id})
                output.append(item)
            result[key] = output

        elif key in ["collection_tags"]:
            result[key] = _generate_hierarchical_structure(value)

        elif key in ["resources"]:
            result[key] = value

        # If key is dict
        elif isinstance(value, dict) and key in QUERY_PARAMS:
            # If id-dict
            if value.get("id"):
                _id = value.get("id")
                label = value.get("label")
                item = {}
                item["label"] = label
                item["id"] = _id
                item["new_link"] = urlencode({key: _id})
                result[key] = item
            else:
                result[key] = value

        # If key is list (of id-dicts)
        elif isinstance(value, list) and key in QUERY_PARAMS:
            output = []

            for _dict in value:

                # hierarchical concept or entity
                if isinstance(_dict.get("id"), list):
                    hierarchy = []
                    for i, v in enumerate(_dict.get("id")):
                        item = {}
                        item["id"] = v
                        item["label"] = _dict.get("label")[i]
                        item["new_link"] = "=".join([key, str(v)])
                        hierarchy.append(item)
                    output.append(hierarchy)

                # flat concept or entity
                else:
                    _id = _dict.get("id")
                    label = _dict.get("label")
                    item = {}
                    item["id"] = _id
                    item["label"] = label
                    item["new_link"] = urlencode({key: _id})
                    output.append(item)

            result[key] = output

        else:
            result[key] = value

    return result
