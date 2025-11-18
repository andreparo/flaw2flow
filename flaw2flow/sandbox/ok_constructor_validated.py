from flaw2flow.f2f import F2F


class Person:
    """
    Class with properly validated constructor.

    F2FGuard should accept this class.
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
        F2F.validate_String(name)

        self.age = age
        self.name = name
