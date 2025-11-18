from flaw2flow.f2f import F2F


def foo(x: int | float) -> float:
    """MUST FAIL — only validates int, missing Float validator."""
    F2F.validate_Int(x)
    return float(x)
