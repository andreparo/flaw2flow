from flaw2flow.f2f import F2F


def check(b: bool) -> bool:
    """MUST FAIL — wrong validator."""
    F2F.validate_Int(b)
    return b
