from flaw2flow.f2f import F2F


def foo(x: int | str) -> int | str:
    """
    Missing one validation for a union type parameter (int | str).

    Required:
    - validate_Int
    - validate_String

    Only validate_Int is present → should fail.

    Parameters
    ----------
    x : int | str
        Value to validate.

    Returns
    -------
    int | str
        The input value.
    """
    F2F.validate_Int(x)
    return x
