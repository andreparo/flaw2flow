from flaw2flow.f2f import F2F


def foo(lst: list[str]) -> list[str]:
    """MUST FAIL — numeric validator used."""
    F2F.validate_Numeric_List(lst)
    return lst
