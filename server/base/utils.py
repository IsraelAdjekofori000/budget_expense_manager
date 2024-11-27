def value_or_default(_callable, default, **kwargs):
    """
    provides a default value if an error occurred while running func
    """

    try:
        return _callable(**kwargs), None
    except Exception as e:
        return default, e
