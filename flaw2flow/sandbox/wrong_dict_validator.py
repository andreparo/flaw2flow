from flaw2flow.f2f import F2F


def foo(d: dict) -> dict:
    """MUST FAIL — wrong validator."""
    F2F.validate_List(d)
    return d
