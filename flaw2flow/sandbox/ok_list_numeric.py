from flaw2flow.f2f import F2F


def foo(xs: list[int]) -> int:
    """
    Correct validation for list[int] → requires validate_Numeric_List.

    This should pass.

    Parameters
    ----------
    xs : list[int]
        List of integers to validate.

    Returns
    -------
    int
        Sum of the list.
    """
    F2F.validate_Numeric_List(xs)
    return sum(xs)
