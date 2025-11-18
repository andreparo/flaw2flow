from flaw2flow.f2f import F2F


def foo(b: bytes) -> bytes:
    """MUST FAIL."""
    F2F.validate_String(b)
    return b
