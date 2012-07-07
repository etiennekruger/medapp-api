def get_value(value, *keys):
    try:
        for key in keys:
            value = value[key]
        value = '' if value is None else value
    except Exception, e:
        value = ''
    return value

