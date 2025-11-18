from flaw2flow.f2f import F2F


def check(b: bool) -> bool:
    """Should PASS."""
    F2F.validate_Bool(b)
    return b
