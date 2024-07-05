
def get_filter_by_args(args: dict, model_class):
    filters = []
    for key, value in args.items():
        print(value)
        if key.endswith('__gt'):
            key = key.replace("__gt", "")
            filters.append(getattr(model_class, key) > value)
        elif key.endswith('__lt'):
            key = key.replace("__lt", "")
            filters.append(getattr(model_class, key) < value)
        elif key.endswith('__gte'):
            key = key.replace("__gte", "")
            filters.append(getattr(model_class, key) >= value)
        elif key.endswith('__lte'):
            key = key.replace("__lte", "")
            filters.append(getattr(model_class, key) <= value)
    return filters
