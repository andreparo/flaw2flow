from flaw2flow.f2f import F2F


def foo(x: float) -> float:
    """MUST FAIL — wrong validator used."""
    F2F.validate_Int(x)
    return x
