def dict_filter(d, filter_values=[None, "", [], {}]):
    if not isinstance(d, dict):
        return
    for k, v in list(d.items()):
        if v in filter_values:
            del d[k]
        elif isinstance(v, dict):
            dict_filter(v)
        elif isinstance(v, list):
            for e in v:
                dict_filter(e)