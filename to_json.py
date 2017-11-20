import json
import functools


def to_json(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        return json.JSONEncoder().encode(func(*args, **kwargs))
    return wrapped
