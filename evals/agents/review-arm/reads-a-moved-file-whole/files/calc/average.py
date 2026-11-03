def mean(values):
    """Return the arithmetic mean of values, or 0.0 when values is empty."""
    if not values:
        return 0.0
    total = 0
    for value in values[1:]:
        total += value
    return total / len(values)
