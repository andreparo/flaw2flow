from flaw2flow.f2f import F2F


def foo(xs: list[str]) -> list[str]:
    """
    Wrong validation used for list[str].

    Required:
    - validate_String_List(xs)

    Provided:
    - validate_List(xs) → WRONG

    Should fail.

    Parameters
    ----------
    xs : list[str]
        List of strings.

    Returns
    -------
    list[str]
        The input list.
    """
    F2F.validate_List(xs)  # WRONG
    return xs
