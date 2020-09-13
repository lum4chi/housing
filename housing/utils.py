def dict_filter(d, values=[None, "", [], {}]):
    if not isinstance(d, dict):
        return
    for k, v in list(d.items()):
        if v in values:
            del d[k]
        elif isinstance(v, dict):
            dict_filter(v)
        elif isinstance(v, list):
            for e in v:
                dict_filter(e)