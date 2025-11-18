from flaw2flow.f2f import F2F


def foo(lst: list[str]) -> list[str]:
    """Should PASS — string list, so validate_String_List."""
    F2F.validate_String_List(lst)
    return lst
