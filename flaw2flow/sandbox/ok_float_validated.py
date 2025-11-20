from flaw2flow.f2f import F2F
from datetime import datetime


def foo(x: float, y: datetime) -> float:
    """Should PASS — float validated correctly."""
    F2F.validate_Float(x)
    return x
