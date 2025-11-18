from flaw2flow.f2f import F2F


class Person:
    """
    Class constructor missing one required validation.

    Required:
    - validate_Int(age)
    - validate_String(name)

    validate_String is missing → should fail.
    """

    def __init__(self, age: int, name: str) -> None:
        """
        Parameters
        ----------
        age : int
            Age value.
        name : str
            Person name.
        """
        F2F.validate_Int(age)
        # missing validate_String(name)

        self.age = age
        self.name = name
