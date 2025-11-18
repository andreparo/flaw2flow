from flaw2flow.f2f import F2F


def foo(x: int) -> int:
    """
    Wrong validator applied to an integer parameter.

    F2FGuard should raise an error:
    - unexpected validator validate_String

    Parameters
    ----------
    x : int
        Integer that should be validated with validate_Int.

    Returns
    -------
    int
        The input value.
    """
    F2F.validate_String(x)  # WRONG
    return x
