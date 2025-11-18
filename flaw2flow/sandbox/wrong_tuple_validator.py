from flaw2flow.f2f import F2F


def foo(t: tuple) -> tuple:
    """MUST FAIL — wrong validator."""
    F2F.validate_List(t)
    return t
