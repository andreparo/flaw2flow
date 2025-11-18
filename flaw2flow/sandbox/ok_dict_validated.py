from flaw2flow.f2f import F2F


def foo(d: dict) -> dict:
    """Should PASS."""
    F2F.validate_Dict(d)
    return d
