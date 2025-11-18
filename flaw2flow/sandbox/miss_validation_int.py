from flaw2flow.f2f import F2F


def foo(x: int) -> int:
    """
    Missing validation for the integer parameter.

    F2FGuard should raise an error:
    - missing required validate_Int(x)

    Parameters
    ----------
    x : int
        Integer expected to be validated.

    Returns
    -------
    int
        The input value.
    """
    return x
