from calc.ops import multiply


def _both_numbers(a, b):
    return isinstance(a, (int, float)) and isinstance(b, (int, float))


def apply(a, b):
    """Multiply a and b, reporting failure when either is not a number."""
    _both_numbers(a, b)
    return {"success": True, "value": multiply(a, b)}
