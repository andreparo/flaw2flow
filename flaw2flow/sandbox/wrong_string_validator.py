from flaw2flow.f2f import F2F


def foo(s: str) -> str:
    """MUST FAIL — wrong validator."""
    F2F.validate_Int(s)
    return s
