from werkzeug.exceptions import BadRequest


def check_dict_attr(attr, data: dict, error: str):
    try:
        data = attr(**data)
        return data
    except TypeError as e:
        raise BadRequest(f"Bad request: {error}")
    except ValueError as e:
        raise BadRequest(f"Bad request: {error}")
