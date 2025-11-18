class F2FGuard:
    """
    Performs validation coverage checks for functions and classes.

    Rules enforced:
    - Every function parameter must be either:
        • a builtin/external object,
        • a custom object whose constructor has already been validated,
        • or a builtin data type validated inside the function body: str, float, bool, int, list, dict
    - Every custom object constructor must itself perform F2F validation.
    """
