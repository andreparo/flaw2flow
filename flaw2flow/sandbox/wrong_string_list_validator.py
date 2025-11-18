from flaw2flow.f2f import F2F


def foo(lst: list[str]) -> list[str]:
    """MUST FAIL — wrong validator."""
    F2F.validate_List(lst)
    return lst
