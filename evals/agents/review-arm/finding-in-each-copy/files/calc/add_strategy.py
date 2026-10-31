from calc.ops import add


def _both_numbers(a, b):
    return isinstance(a, (int, float)) and isinstance(b, (int, float))


def apply(a, b):
    """Add a and b, reporting failure when either is not a number."""
    _both_numbers(a, b)
    return {"success": True, "value": add(a, b)}
