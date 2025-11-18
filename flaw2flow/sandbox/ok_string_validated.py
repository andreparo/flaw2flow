from flaw2flow.f2f import F2F


def foo(s: str) -> str:
    """Should PASS."""
    F2F.validate_String(s)
    return s
