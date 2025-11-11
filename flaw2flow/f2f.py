from typing import Any, Sequence


class F2F:
    """Class providing general purpose validators"""

    @classmethod
    def validate_Int(
        cls,
        target: Any,
        *,
        positive: bool = False,
        negative: bool = False,
        positive_0: bool = False,
        negative_0: bool = False,
        non_0: bool = False,
        even: bool = False,
        odd: bool = False,
        min_value: int | None = None,
        max_value: int | None = None,
        value_range: tuple[int, int] | None = None,
        divisors: Sequence[int] | None = None,
        multiples: Sequence[int] | None = None,
        prime: bool = False,
        composite: bool = False,
        allowed: Sequence[int] | None = None,
    ) -> None:
        """Validate integers

        - positive: bool
        - negative: bool
        - positive_0: bool
        - negative_0: bool
        - non_0: bool
        - even: bool
        - odd: bool
        - min_value: int
        - max_value: int
        - range: tuple as (min: int, max: int)
        - divisors: Sequence(int)
        - multiples: Sequence(int)
        - prime: bool
        - composite: bool
        - allowed: Sequence(int)


        # --- Positive / Negative Variants ---
        >>test:  cls.validate_Int(5, positive=True) is None
        >>error: cls.validate_Int(-1, positive=True)

        >>test:  cls.validate_Int(-5, negative=True) is None
        >>error: cls.validate_Int(3, negative=True)

        >>test:  cls.validate_Int(0, positive_0=True) is None
        >>error: cls.validate_Int(-5, positive_0=True)

        >>test:  cls.validate_Int(0, negative_0=True) is None
        >>error: cls.validate_Int(4, negative_0=True)

        >>test:  cls.validate_Int(3, non_0=True) is None
        >>error: cls.validate_Int(0, non_0=True)

        # --- Even / Odd ---
        >>test:  cls.validate_Int(8, even=True) is None
        >>error: cls.validate_Int(7, even=True)

        >>test:  cls.validate_Int(7, odd=True) is None
        >>error: cls.validate_Int(6, odd=True)

        # --- Min / Max / Range ---
        >>test:  cls.validate_Int(5, min_value=2) is None
        >>error: cls.validate_Int(1, min_value=2)

        >>test:  cls.validate_Int(5, max_value=10) is None
        >>error: cls.validate_Int(12, max_value=10)

        >>error:  cls.validate_Int(5, value_range=(1, 10))
        >>error: cls.validate_Int(0, value_range=(1, 10))

        # --- Divisors / Multiples ---
        >>test:  cls.validate_Int(12, divisors=[2, 3]) is None
        >>error: cls.validate_Int(12, divisors=[5])

        >>test:  cls.validate_Int(3, multiples=[6, 9]) is None
        >>error: cls.validate_Int(4, multiples=[6, 9])

        # --- Prime / Composite ---
        >>test:  cls.validate_Int(7, prime=True) is None
        >>error: cls.validate_Int(8, prime=True)

        >>test:  cls.validate_Int(9, composite=True) is None
        >>error: cls.validate_Int(7, composite=True)

        # --- Allowed List ---
        >>test:  cls.validate_Int(20, allowed=[10, 20, 30]) is None
        >>error: cls.validate_Int(25, allowed=[10, 20, 30])

        # --- Type Checking ---
        >>error: cls.validate_Int("5", positive=True)
        >>error: cls.validate_Int(True, positive=True)
        >>error: cls.validate_Int(3.0, positive=True)
        >>test:  cls.validate_Int(3, positive=True) is None

        """

        # --- Type and base validation ---
        if not isinstance(target, int) or isinstance(target, bool):
            raise TypeError(f"Expected int, got {type(target).__name__}")

        # --- Basic value checks ---
        if positive and target <= 0:
            raise ValueError("Value must be positive")

        if negative and target >= 0:
            raise ValueError("Value must be negative")

        if positive_0 and target < 0:
            raise ValueError("Value must be positive or zero")

        if negative_0 and target > 0:
            raise ValueError("Value must be negative or zero")

        if non_0 and target == 0:
            raise ValueError("Value must be non-zero")

        # --- Parity checks ---
        if even and target % 2 != 0:
            raise ValueError("Value must be even")

        if odd and target % 2 == 0:
            raise ValueError("Value must be odd")

        # --- Range checks ---
        if min_value is not None and target < min_value:
            raise ValueError(f"Value must be >= {min_value}")

        if max_value is not None and target > max_value:
            raise ValueError(f"Value must be <= {max_value}")

        if value_range is not None:
            min_r, max_r = value_range
            if target < min_r or target > max_r:
                raise ValueError(f"Value must be within range ({min_r}, {max_r})")

        # --- Divisors and multiples checks ---
        if divisors:
            for divisor in divisors:
                if divisor == 0:
                    raise ValueError("Divisor cannot be zero")
                if target % divisor != 0:
                    raise ValueError(f"Value must be divisible by {divisor}")

        if multiples:
            for multiple in multiples:
                if multiple == 0:
                    raise ValueError("Multiple cannot be zero")
                if multiple % target != 0:
                    raise ValueError(f"Value must be a divisor of {multiple}")

        # --- Primality and compositeness checks ---
        if prime:
            if target < 2:
                raise ValueError("Value must be a prime number")
            for i in range(2, int(target**0.5) + 1):
                if target % i == 0:
                    raise ValueError("Value must be a prime number")

        if composite:
            if target <= 1:
                raise ValueError("Value must be a composite number")
            if all(target % i != 0 for i in range(2, int(target**0.5) + 1)):
                raise ValueError("Value must be a composite number")

        # --- Allowed values check ---
        if allowed is not None and target not in allowed:
            raise ValueError(f"Value must be one of {allowed}")
