from flaw2flow.f2f import F2F


def foo(x: int | float) -> float:
    """Should PASS — both validators present."""
    F2F.validate_Int(x)
    F2F.validate_Float(x)
    return float(x)
