from flaw2flow.f2f import F2F


def foo(x: int) -> int:
    """
    Simple function that validates an integer parameter using the correct
    F2F validator. This function should pass F2FGuard validation checks.

    Parameters
    ----------
    x : int
        Integer value to validate.

    Returns
    -------
    int
        The input value incremented by one.
    """
    F2F.validate_Int(x)
    return x + 1
