from flaw2flow.f2f import F2F


def foo(t: tuple) -> tuple:
    """Should PASS."""
    F2F.validate_Tuple(t)
    return t
