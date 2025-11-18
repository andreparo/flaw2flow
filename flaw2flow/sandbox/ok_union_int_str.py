from flaw2flow.f2f import F2F


def foo(x: int | str) -> int | str:
    """
    Correct validation for a union type parameter (int | str).

    Required validators:
    - validate_Int
    - validate_String

    All validations are correctly applied, so this should pass.

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
    F2F.validate_String(x)
    return x
