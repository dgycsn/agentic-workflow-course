import inspect

def schema_from_function(func):
    """
    inspect function and create dict for its inputs
    """
    sig = inspect.signature(func)

    properties = {}
    required = []

    for name, param in sig.parameters.items():
        # default → required or not
        if param.default is inspect.Parameter.empty:
            required.append(name)

        # type annotation
        annotation = param.annotation
        if annotation is inspect.Parameter.empty:
            json_type = "string"   # fallback
        elif annotation is str:
            json_type = "string"
        elif annotation is int:
            json_type = "integer"
        elif annotation is float:
            json_type = "number"
        elif annotation is bool:
            json_type = "boolean"
        else:
            json_type = "object"

        properties[name] = {"type": json_type}

    return {
        "type": "object",
        "properties": properties,
        "required": required,
    }