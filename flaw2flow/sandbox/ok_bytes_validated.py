from flaw2flow.f2f import F2F


def foo(b: bytes) -> bytes:
    """Should PASS."""
    F2F.validate_Bytes(b)
    return b
