from flaw2flow.f2f import F2F


def foo(x: float) -> float:
    """Should PASS — float validated correctly."""
    F2F.validate_Float(x)
    return x
