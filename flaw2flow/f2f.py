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
        str_min_length: int | None = None,
        str_max_length: int | None = None,
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
        - str_min_length: int
        - str_max_length: int
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

        # --- Check length when converted to a string
        if str_min_length is not None:
            if len(str(target)) < str_min_length:
                raise ValueError(
                    f"Value must have a length longer or equal to {str_min_length=} when converted to string: {len(str(target))=}"
                )

        if str_max_length is not None:
            if len(str(target)) > str_max_length:
                raise ValueError(
                    f"Valuemust have a length shorter or equal to {str_max_length=} when converted to string: {len(str(target))=}"
                )

    """
    DOCCHECK TESTS:

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

    >>test:  cls.validate_Int(5, value_range=(1, 10)) is None
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

    # -- String max length
    >>error: cls.validate_Int(12345, str_max_length=4)
    >>test: cls.validate_Int(12345, str_max_length=5) is None
    >>test: cls.validate_Int(12345, str_max_length=6) is None

    # --- Type Checking ---
    >>error: cls.validate_Int("5", positive=True)
    >>error: cls.validate_Int(True, positive=True)
    >>error: cls.validate_Int(3.0, positive=True)
    >>test:  cls.validate_Int(3, positive=True) is None
    
    """

    @classmethod
    def validate_Float(
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
        allowed: Sequence[int] | None = None,
        str_min_length: int | None = None,
        str_max_length: int | None = None,
    ) -> None:
        """Validate floats

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
        - prime: bool
        - composite: bool
        - allowed: Sequence(int)
        - str_min_length: int pay attention to scientific notation
        - str_max_length: int pay attention to scientific notation
        """

        # --- Type and base validation ---
        if not (isinstance(target, (float, int))) or isinstance(target, bool):
            raise TypeError(f"Expected float, got {type(target).__name__}")

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

        # --- Allowed values check ---
        if allowed is not None and target not in allowed:
            raise ValueError(f"Value must be one of {allowed}")

        # --- Check length when converted to a string
        if str_min_length is not None:
            if len(str(target)) < str_min_length:
                raise ValueError(
                    f"Value must have a length longer or equal to {str_min_length=} when converted to string: {len(str(target))=}"
                )

        if str_max_length is not None:
            if len(str(target)) > str_max_length:
                raise ValueError(
                    f"Valuemust have a length shorter or equal to {str_max_length=} when converted to string: {len(str(target))=}"
                )

    """
    DOCCHECK TESTS:

    # --- Positive / Negative Variants ---
    >>test:  cls.validate_Float(5.5, positive=True) is None
    >>error: cls.validate_Float(-1.2, positive=True)

    >>test:  cls.validate_Float(-5.1, negative=True) is None
    >>error: cls.validate_Float(3.4, negative=True)

    >>test:  cls.validate_Float(0.0, positive_0=True) is None
    >>error: cls.validate_Float(-5.0, positive_0=True)

    >>test:  cls.validate_Float(0.0, negative_0=True) is None
    >>error: cls.validate_Float(4.3, negative_0=True)

    >>test:  cls.validate_Float(3.3, non_0=True) is None
    >>error: cls.validate_Float(0.0, non_0=True)

    # --- Even / Odd ---
    >>test:  cls.validate_Float(8.0, even=True) is None
    >>error: cls.validate_Float(7.0, even=True)

    >>test:  cls.validate_Float(7.0, odd=True) is None
    >>error: cls.validate_Float(6.0, odd=True)

    # --- Min / Max / Range ---
    >>test:  cls.validate_Float(5.5, min_value=2.2) is None
    >>error: cls.validate_Float(1.1, min_value=2.2)

    >>test:  cls.validate_Float(5.5, max_value=10.0) is None
    >>error: cls.validate_Float(12.5, max_value=10.0)

    >>test:  cls.validate_Float(5.5, value_range=(1.0, 10.0)) is None
    >>error: cls.validate_Float(0.5, value_range=(1.0, 10.0))
    >>error: cls.validate_Float(11.0, value_range=(1.0, 10.0))

    # --- Allowed List ---
    >>test:  cls.validate_Float(20.0, allowed=[10.0, 20.0, 30.0]) is None
    >>error: cls.validate_Float(25.0, allowed=[10.0, 20.0, 30.0])

    # -- String max length
    >>error: cls.validate_Float(12345.0, str_max_length=4)
    >>test: cls.validate_Float(12345, str_max_length=5) is None
    >>test: cls.validate_Float(12345.4, str_max_length=10) is None
    >>error: cls.validate_Float(0.003003, str_max_length=6)

    # --- Type Checking ---
    >>error: cls.validate_Float("5.0", positive=True)
    >>error: cls.validate_Float(True, positive=True)
    >>error: cls.validate_Float(None, positive=True)
    >>test:  cls.validate_Float(3.0, positive=True) is None
    """

    @classmethod
    def validate_Bool(
        cls,
        target: Any,
        *,
        must_be_true: bool = False,
        must_be_false: bool = False,
    ) -> None:
        """Validate booleans

        - must_be_true: bool → ensures value is True
        - must_be_false: bool → ensures value is False
        """

        # --- Type check ---
        if not isinstance(target, bool):
            raise TypeError(f"Expected bool, got {type(target).__name__}")

        # --- Value checks ---
        if must_be_true and target is not True:
            raise ValueError("Value must be True")

        if must_be_false and target is not False:
            raise ValueError("Value must be False")

    """
    DOCCHECK TESTS:

    >>test: cls.validate_Bool(True) is None
    >>test: cls.validate_Bool(False) is None
    >>test: cls.validate_Bool(True, must_be_true=True) is None
    >>error: cls.validate_Bool(False, must_be_true=True)
    >>test: cls.validate_Bool(False, must_be_false=True) is None
    >>error: cls.validate_Bool(True, must_be_false=True)
    """

    @classmethod
    def validate_String(
        cls,
        target: Any,
        *,
        min_length: int | None = None,
        max_length: int | None = None,
        range_length: tuple[int, int] | None = None,
        starts_with: str | None = None,
        does_not_start_with: str | None = None,
        ends_with: str | None = None,
        does_not_end_with: str | None = None,
        contains: str | Sequence[str] | None = None,
        allowed: Sequence[str] | None = None,
        forbidden: Sequence[str] | None = None,
        must_be_lowercase: bool = False,
        must_be_uppercase: bool = False,
        allow_alphabetic: bool = True,
        allow_numeric: bool = True,
        allow_special: bool = True,
        allow_whitespaces: bool = True,
        allow_empty: bool = False,
        no_consecutive_spaces: bool = False,
        regex: str | None = None,
        not_regex: str | None = None,
        json_safe: bool = False,
        ascii_only: bool = False,
    ) -> None:
        """Validate string values.

        Performs a variety of checks to ensure the string meets the defined
        rules for content, structure, and allowed characters.

        Parameters:
        ----------
        target : Any
            Value to validate. Must be of type `str`.
        min_length : int | None
            Minimum allowed length (inclusive).
        max_length : int | None
            Maximum allowed length (inclusive).
        range_length : tuple[int, int] | None
            Required inclusive length range (min, max).
        starts_with : str | None
            Required starting substring.
        does_not_start_with : str | None
            Forbidden starting substring.
        ends_with : str | None
            Required ending substring.
        does_not_end_with : str | None
            Forbidden ending substring.
        contains : str | Sequence[str] | None
            Required substring or list of substrings that must appear.
        allowed : Sequence[str] | None
            Whitelist of allowed exact strings.
        forbidden : Sequence[str] | None
            Blacklist of disallowed exact strings.
        must_be_lowercase : bool
            Require the entire string to be lowercase.
        must_be_uppercase : bool
            Require the entire string to be uppercase.
        allow_alphabetic : bool
            Allow alphabetic characters (a–z, A–Z).
        allow_numeric : bool
            Allow numeric characters (0–9).
        allow_special : bool
            Allow special characters (punctuation).
        allow_whitespaces : bool
            Allow space characters.
        allow_empty : bool
            Allow empty string values.
        no_consecutive_spaces : bool
            Disallow consecutive spaces ("  ").
        regex : str | None
            Regex pattern the string must match entirely.
        not_regex : str | None
            Regex pattern the string must *not* match entirely.
        json_safe : bool
            Ensure the string is JSON-encodable and contains no control characters.
        ascii_only : bool
            Require all characters to be ASCII.
        """

        import re
        import string
        import json

        # --- Type check ---
        if not isinstance(target, str):
            raise TypeError(f"Expected str, got {type(target).__name__}")

        # --- Empty string check ---
        if not allow_empty and len(target) == 0:
            raise ValueError("Empty strings are not allowed")

        # --- Length checks ---
        if min_length is not None and len(target) < min_length:
            raise ValueError(f"String must be at least {min_length} characters long")

        if max_length is not None and len(target) > max_length:
            raise ValueError(f"String must be at most {max_length} characters long")

        if range_length is not None:
            min_r, max_r = range_length
            if not min_r <= len(target) <= max_r:
                raise ValueError(f"String length must be within range ({min_r}, {max_r})")

        # --- Start / End checks ---
        if starts_with is not None and not target.startswith(starts_with):
            raise ValueError(f"String must start with '{starts_with}'")

        if does_not_start_with is not None and target.startswith(does_not_start_with):
            raise ValueError(f"String must not start with '{does_not_start_with}'")

        if ends_with is not None and not target.endswith(ends_with):
            raise ValueError(f"String must end with '{ends_with}'")

        if does_not_end_with is not None and target.endswith(does_not_end_with):
            raise ValueError(f"String must not end with '{does_not_end_with}'")

        # --- Contains checks ---
        if contains is not None:
            if isinstance(contains, str):
                contains = [contains]
            for substring in contains:
                if substring not in target:
                    raise ValueError(f"String must contain '{substring}'")

        # --- Case checks ---
        if must_be_lowercase and not target.islower():
            raise ValueError("String must be all lowercase")

        if must_be_uppercase and not target.isupper():
            raise ValueError("String must be all uppercase")

        # --- ASCII check ---
        if ascii_only and not target.isascii():
            raise ValueError("String must contain only ASCII characters")

        # --- No consecutive spaces check ---
        if no_consecutive_spaces and "  " in target:
            raise ValueError("String must not contain consecutive spaces")

        # --- Allowed composition checks ---

        allowed_chars: set[str] = set()
        if allow_alphabetic:
            allowed_chars.update(string.ascii_letters)
        if allow_numeric:
            allowed_chars.update(string.digits)
        if allow_special:
            allowed_chars.update(string.punctuation)
        if allow_whitespaces:
            allowed_chars.add(" ")

        for char in target:
            if char not in allowed_chars:
                raise ValueError(f"Invalid character '{char}' not allowed by composition rules")

        # --- JSON safety check ---
        if json_safe:
            try:
                json.dumps(target)
            except Exception:
                raise ValueError("String contains characters not safe for JSON encoding")

            # Check for unescaped control characters
            if any(ord(c) < 32 and c not in "\t\n\r" for c in target):
                raise ValueError("String contains non-printable control characters")

        # --- Regex checks ---
        if regex is not None:
            if re.fullmatch(regex, target) is None:
                raise ValueError(f"String does not match required pattern: {regex}")

        if not_regex is not None:
            if re.fullmatch(not_regex, target) is not None:
                raise ValueError(f"String matches forbidden pattern: {not_regex}")

        # --- Allowed / Forbidden lists ---
        if allowed is not None and target not in allowed:
            raise ValueError(f"String must be one of {allowed}")

        if forbidden is not None and target in forbidden:
            raise ValueError(f"String must not be one of {forbidden}")

    """
    DOCCHECK TESTS:

    # --- Type ---
    >>test: cls.validate_String("hello") is None
    >>error: cls.validate_String(123)

    # --- Length ---
    >>test: cls.validate_String("abc", min_length=2) is None
    >>error: cls.validate_String("a", min_length=2)
    >>error: cls.validate_String("abc", max_length=2) 
    >>test: cls.validate_String("a", max_length=2) is None
    >>test: cls.validate_String("abc", range_length=(2,4)) is None
    >>error: cls.validate_String("a", range_length=(2,4))
    >>error: cls.validate_String("abcdefg", range_length=(2,4))

    # --- Start / End ---
    >>test: cls.validate_String("python_code", starts_with="py") is None
    >>error: cls.validate_String("python_code", starts_with="js")
    >>test: cls.validate_String("file.txt", ends_with=".txt") is None
    >>error: cls.validate_String("file.txt", ends_with=".csv")
    >>test: cls.validate_String("hello_world", does_not_start_with="test") is None
    >>error: cls.validate_String("test_case", does_not_start_with="test")
    >>test: cls.validate_String("file.log", does_not_end_with=".txt") is None
    >>error: cls.validate_String("file.txt", does_not_end_with=".txt")

    # --- Contains ---
    >>test: cls.validate_String("data_validator", contains="data") is None
    >>error: cls.validate_String("validator", contains="data")
    >>test: cls.validate_String("data_validator", contains=["data", "val", "a_v", "data_validator"]) is None
    >>error: cls.validate_String("validator", contains=["validator","toree", "val", "a_v"])

    # --- Case ---
    >>test: cls.validate_String("lowercase", must_be_lowercase=True) is None
    >>error: cls.validate_String("MixedCase", must_be_lowercase=True)
    >>error: cls.validate_String("UPPER", must_be_lowercase=True)
    >>test: cls.validate_String("UPPER", must_be_uppercase=True) is None
    >>error: cls.validate_String("NotUpper", must_be_uppercase=True)
    >>error: cls.validate_String("lowercase", must_be_uppercase=True)

    # --- ASCII ---
    >>test: cls.validate_String("ascii_only", ascii_only=True) is None
    >>error: cls.validate_String("café", ascii_only=True)

    # --- No consecutive spaces ---
    >>test: cls.validate_String("Hello world", no_consecutive_spaces=True) is None
    >>error: cls.validate_String("Hello  world", no_consecutive_spaces=True)

    # --- JSON safety ---
    >>test: cls.validate_String("safe string", json_safe=True) is None
    >>error: cls.validate_String("unsafe \x07 char", json_safe=True)

    # --- Allowed composition ---
        # --- Allowed Composition Rules ---

    # Default behavior: allows everything (letters, digits, punctuation, spaces)
    >>test: cls.validate_String("Abc 123!?") is None
    >>error: cls.validate_String("")  # default disallows empty string

    # --- Alphabetic Control ---
    # Only alphabetic disabled → should reject letters
    >>error: cls.validate_String("abc", allow_alphabetic=False)
    >>test: cls.validate_String("1234", allow_alphabetic=False) is None
    >>test: cls.validate_String("!@#$", allow_alphabetic=False) is None

    # Alphabetic only → reject digits and symbols
    >>test: cls.validate_String("Hello", allow_numeric=False, allow_special=False, allow_whitespaces=False) is None
    >>error: cls.validate_String("Hello1", allow_numeric=False)
    >>error: cls.validate_String("Hello!", allow_special=False)

    # --- Numeric Control ---
    # Only numeric disabled → should reject digits
    >>error: cls.validate_String("1234", allow_numeric=False)
    >>test: cls.validate_String("abcd", allow_numeric=False) is None
    >>test: cls.validate_String("!@#$", allow_numeric=False) is None

    # Numeric only → reject everything else
    >>test: cls.validate_String("98765", allow_alphabetic=False, allow_special=False, allow_whitespaces=False) is None
    >>error: cls.validate_String("9876a", allow_alphabetic=False)
    >>error: cls.validate_String("98 76", allow_whitespaces=False)

    # --- Special Character Control ---
    # Only special disabled → should reject punctuation
    >>error: cls.validate_String("abc!", allow_special=False)
    >>test: cls.validate_String("abc123", allow_special=False) is None

    # Special only → only punctuation allowed
    >>test: cls.validate_String("!@#$", allow_alphabetic=False, allow_numeric=False, allow_whitespaces=False) is None
    >>error: cls.validate_String("!@#a", allow_alphabetic=False)

    # --- Whitespace Control ---
    # Only whitespaces disabled → reject strings with spaces
    >>error: cls.validate_String("has space", allow_whitespaces=False)
    >>test: cls.validate_String("no_space", allow_whitespaces=False) is None

    # Whitespaces only (useful for testing pure-space input)
    >>test: cls.validate_String("   ", allow_alphabetic=False, allow_numeric=False, allow_special=False) is None
    >>error: cls.validate_String("a ", allow_alphabetic=False)

    # --- Mixed Combinations ---
    # Letters + Digits (common identifier pattern)
    >>test: cls.validate_String("A1b2C3", allow_special=False, allow_whitespaces=False) is None
    >>error: cls.validate_String("A1b2!", allow_special=False)

    # Letters + Special (password-like pattern)
    >>test: cls.validate_String("Hello!", allow_numeric=False) is None
    >>error: cls.validate_String("Hello1", allow_numeric=False)

    # Digits + Special
    >>test: cls.validate_String("123!", allow_alphabetic=False, allow_whitespaces=False) is None
    >>error: cls.validate_String("123a!", allow_alphabetic=False)

    # Digits + Spaces
    >>test: cls.validate_String("12 34", allow_alphabetic=False, allow_special=False) is None
    >>error: cls.validate_String("12a34", allow_alphabetic=False, allow_special=False)

    # --- Strict All Disabled ---
    # When all categories disabled, nothing but empty string could pass (and allow_empty must be True)
    >>test: cls.validate_String("", allow_empty=True, allow_alphabetic=False, allow_numeric=False, allow_special=False, allow_whitespaces=False) is None
    >>error: cls.validate_String("a", allow_empty=True, allow_alphabetic=False, allow_numeric=False, allow_special=False, allow_whitespaces=False)

    # --- Regex ---
    >>test: cls.validate_String("abc123", regex="^[a-z]+\\d+$") is None
    >>error: cls.validate_String("123abc", regex="^[a-z]+\\d+$")

    # --- Allowed / Forbidden ---
    >>test: cls.validate_String("yes", allowed=["yes","no"]) is None
    >>error: cls.validate_String("maybe", allowed=["yes","no"])
    >>test: cls.validate_String("safe", forbidden=["danger","alert"]) is None
    >>error: cls.validate_String("alert", forbidden=["danger","alert"])
    """

    @classmethod
    def validate_Dict(
        cls,
        target: Any,
        schema: dict[str, type | tuple[type, ...]] | None = None,
        *,
        allow_other_keys: bool = False,
        keys_must_be_strings: bool = True,
    ) -> None:
        """Validate dictionaries according to a schema definition.

        Parameters
        ----------
        target : Any
            The object to validate, must be of type `dict`.
        schema : dict[str, type | tuple[type, ...]] | None
            Expected dictionary schema, mapping keys to allowed types or tuple of allowed types.
            Example:
                {"name": str, "age": (int, float)}
        allow_other_keys : bool
            Whether to allow keys that are not defined in the schema.
        keys_must_be_strings : bool
            If True, enforces that all dictionary keys are strings.
        """

        # --- Type check ---
        if not isinstance(target, dict):
            raise TypeError(f"Expected dict, got {type(target).__name__}")

        # --- Key type enforcement ---
        if keys_must_be_strings:
            for key in target.keys():
                if not isinstance(key, str):
                    raise TypeError(f"All keys must be strings, got key of type {type(key).__name__}: {key!r}")

        # --- If schema is provided, perform schema validation ---
        if schema is not None:
            # --- Schema key type check ---
            for schema_key in schema.keys():
                if not isinstance(schema_key, str):
                    raise TypeError(f"Schema key must be a string, got {type(schema_key).__name__}")

            # --- Check each key in target dict ---
            for key, value in target.items():
                if key not in schema:
                    if not allow_other_keys:
                        raise KeyError(f"Unexpected key '{key}' found in dictionary")
                    # skip validation for keys outside schema if allowed
                    continue

                expected_type = schema[key]

                # normalize to tuple for uniformity
                if not isinstance(expected_type, tuple):
                    expected_type = (expected_type,)

                if not isinstance(value, expected_type):
                    expected_names = ", ".join(t.__name__ for t in expected_type)
                    raise TypeError(f"Key '{key}' expects value of type(s): {expected_names}, " f"but got {type(value).__name__}")

            # --- Ensure all required schema keys are present ---
            for required_key in schema.keys():
                if required_key not in target:
                    raise KeyError(f"Missing required key '{required_key}' in dictionary")

        # --- If schema is None, still ensure all keys are valid strings if required ---
        elif keys_must_be_strings:
            for key in target.keys():
                if not isinstance(key, str):
                    raise TypeError(f"Invalid key type: {type(key).__name__}, expected string")

    """
    DOCCHECK TESTS:

    # --- Basic Type ---
    >>test: cls.validate_Dict({"a": 1}) is None
    >>error: cls.validate_Dict([("a", 1)])

    # --- Key type enforcement ---
    >>test: cls.validate_Dict({"a": 1, "b": 2}, keys_must_be_strings=True) is None
    >>error: cls.validate_Dict({1: "a"}, keys_must_be_strings=True)
    >>test: cls.validate_Dict({1: "a"}, keys_must_be_strings=False) is None

    # --- Schema validation (single type) ---
    >>test: cls.validate_Dict({"a": 1, "b": "text"}, {"a": int, "b": str}) is None
    >>error: cls.validate_Dict({"a": "wrong", "b": "text"}, {"a": int, "b": str})

    # --- Schema validation (tuple of allowed types) ---
    >>test: cls.validate_Dict({"a": 1, "b": 2.5}, {"a": (int, float), "b": (int, float)}) is None
    >>error: cls.validate_Dict({"a": "1"}, {"a": (int, float)})

    # --- Extra keys not allowed ---
    >>error: cls.validate_Dict({"a": 1, "extra": 5}, {"a": int})
    >>test: cls.validate_Dict({"a": 1, "extra": 5}, {"a": int}, allow_other_keys=True) is None

    # --- Missing required key ---
    >>error: cls.validate_Dict({"a": 1}, {"a": int, "b": str})

    # --- Schema with non-string key ---
    >>error: cls.validate_Dict({"a": 1}, {1: int})

    # --- No schema, just key check ---
    >>test: cls.validate_Dict({"x": 10}, keys_must_be_strings=True) is None
    >>error: cls.validate_Dict({10: "value"}, keys_must_be_strings=True)
    """

    @classmethod
    def validate_List(
        cls,
        target: Any,
        *,
        allowed_empty: bool = False,
        min_length: int | None = None,
        max_length: int | None = None,
        allowed_types: type | tuple[type, ...] | None = None,
        allow_duplication: bool = True,
        allowed_values: Sequence[Any] | None = None,
        forbidden_values: Sequence[Any] | None = None,
    ) -> None:
        """Validate list objects.

        Parameters
        ----------
        target : Any
            The object to validate, must be of type `list`.
        allowed_empty : bool
            Whether an empty list is allowed. Defaults to False.
        min_length : int | None
            Minimum number of elements allowed in the list (inclusive).
        max_length : int | None
            Maximum number of elements allowed in the list (inclusive).
        allowed_types : type | tuple[type, ...] | None
            Type or tuple of types allowed for list elements.
            Example: allowed_types=(int, str)
        allow_duplication : bool
            Whether duplicate values are allowed in the list.
        allowed_values : Sequence[Any] | None
            Optional whitelist of permitted element values.
        forbidden_values : Sequence[Any] | None
            Optional blacklist of disallowed element values.
        """

        # --- Type check ---
        if not isinstance(target, list):
            raise TypeError(f"Expected list, got {type(target).__name__}")

        # --- Empty list check ---
        if not allowed_empty and len(target) == 0:
            raise ValueError("Empty lists are not allowed")

        # --- Length checks ---
        if min_length is not None and len(target) < min_length:
            raise ValueError(f"List must contain at least {min_length} elements")

        if max_length is not None and len(target) > max_length:
            raise ValueError(f"List must contain at most {max_length} elements")

        # --- Element type check ---
        if allowed_types is not None:
            if not isinstance(allowed_types, tuple):
                allowed_types = (allowed_types,)
            for index, element in enumerate(target):
                if not isinstance(element, allowed_types):
                    expected_names = ", ".join(t.__name__ for t in allowed_types)
                    raise TypeError(
                        f"Element at index {index} must be of type(s) {expected_names}, " f"but got {type(element).__name__}"
                    )

        # --- Duplication check ---
        if not allow_duplication:
            seen_hashable: set[Any] = set()
            seen_unhashable: list[Any] = []

            for element in target:
                try:
                    # Hashable elements (int, str, tuple, etc.)
                    if element in seen_hashable:
                        raise ValueError(f"Duplicate element '{element}' found in list")
                    seen_hashable.add(element)
                except TypeError:
                    # Unhashable elements (dict, list, set, etc.)
                    for seen in seen_unhashable:
                        if element == seen:
                            raise ValueError("Duplicate elements are not allowed in the list")
                    seen_unhashable.append(element)

        # --- Allowed values check ---
        if allowed_values is not None:
            for element in target:
                if element not in allowed_values:
                    raise ValueError(f"Element {element!r} not in allowed values: {allowed_values}")

        # --- Forbidden values check ---
        if forbidden_values is not None:
            for element in target:
                if element in forbidden_values:
                    raise ValueError(f"Element {element!r} is forbidden by validation rule")

    """
    DOCCHECK TESTS:

    # --- Type ---
    >>test: cls.validate_List([1, 2, 3]) is None
    >>error: cls.validate_List("not a list")

    # --- Empty list ---
    >>error: cls.validate_List([], allowed_empty=False)
    >>test: cls.validate_List([], allowed_empty=True) is None

    # --- Length checks ---
    >>test: cls.validate_List([1, 2], min_length=2) is None
    >>error: cls.validate_List([1], min_length=2)
    >>test: cls.validate_List([1, 2], max_length=2) is None
    >>error: cls.validate_List([1, 2, 3], max_length=2)

    # --- Allowed types ---
    >>test: cls.validate_List([1, 2, 3], allowed_types=int) is None
    >>error: cls.validate_List([1, "a", 3], allowed_types=int)
    >>test: cls.validate_List([1, "a"], allowed_types=(int, str)) is None

    # --- Duplication ---
    >>test: cls.validate_List([1, 2, 3], allow_duplication=True) is None
    >>test: cls.validate_List([1, 2, 3], allow_duplication=False) is None
    >>error: cls.validate_List([1, 2, 1], allow_duplication=False)
    >>error: cls.validate_List([{"a": 1}, {"a": 1}], allow_duplication=False)
    >>test: cls.validate_List([{"a": 1}, {"b": 2}], allow_duplication=False) is None

    # --- Allowed / Forbidden values ---
    >>test: cls.validate_List(["a", "b", "c"], allowed_values=["a", "b", "c", "d"]) is None
    >>error: cls.validate_List(["x", "y"], allowed_values=["a", "b", "c"])
    >>test: cls.validate_List([1, 2, 3], forbidden_values=[9, 10]) is None
    >>error: cls.validate_List([1, 2, 9], forbidden_values=[9, 10])
    """

    @classmethod
    def validate_Numeric_List(
        cls,
        target: Any,
        *,
        allowed_empty: bool = False,
        min_length: int | None = None,
        max_length: int | None = None,
        allow_duplication: bool = True,
        allowed_values: Sequence[float | int] | None = None,
        forbidden_values: Sequence[float | int] | None = None,
        min_value: float | None = None,
        max_value: float | None = None,
        value_range: tuple[float, float] | None = None,
        non_negative: bool = False,
        non_positive: bool = False,
        non_zero: bool = False,
        ascending: bool = False,
        descending: bool = False,
        strictly_ascending: bool = False,
        strictly_descending: bool = False,
        sum_range: tuple[float, float] | None = None,
        mean_range: tuple[float, float] | None = None,
    ) -> None:
        """Validate a list containing numeric (int or float) elements.

        Reuses `validate_List` for structural validation, adding numeric-specific checks
        for bounds, monotonicity, and aggregate constraints. Booleans are not permitted
        even though they subclass int.

        Parameters
        ----------
        target : Any
            The object to validate, must be of type `list`.
        allowed_empty : bool
            Whether an empty list is allowed. Defaults to False.
        min_length : int | None
            Minimum number of elements required in the list.
        max_length : int | None
            Maximum number of elements allowed in the list.
        allow_duplication : bool
            Whether duplicate values are allowed in the list.
        allowed_values : Sequence[float | int] | None
            Optional whitelist of allowed element values.
        forbidden_values : Sequence[float | int] | None
            Optional blacklist of disallowed element values.
        min_value : float | None
            Minimum allowed numeric value for elements.
        max_value : float | None
            Maximum allowed numeric value for elements.
        value_range : tuple[float, float] | None
            Inclusive range (min, max) of allowed element values.
        non_negative : bool
            Ensure all values are >= 0.
        non_positive : bool
            Ensure all values are <= 0.
        non_zero : bool
            Ensure no element is equal to zero.
        ascending : bool
            Require list elements to be non-decreasing (equal values allowed).
        descending : bool
            Require list elements to be non-increasing (equal values allowed).
        strictly_ascending : bool
            Require list elements to be strictly increasing (no equal values).
        strictly_descending : bool
            Require list elements to be strictly decreasing (no equal values).
        sum_range : tuple[float, float] | None
            Inclusive range for total sum of elements.
        mean_range : tuple[float, float] | None
            Inclusive range for arithmetic mean of elements.
        """

        # --- Base structure and type validation ---
        cls.validate_List(
            target,
            allowed_empty=allowed_empty,
            min_length=min_length,
            max_length=max_length,
            allowed_types=(int, float),
            allow_duplication=allow_duplication,
            allowed_values=allowed_values,
            forbidden_values=forbidden_values,
        )

        # --- Ensure no booleans are present (bool is a subclass of int) ---
        for value in target:
            if isinstance(value, bool):
                raise TypeError("Booleans are not allowed in numeric lists")

        # --- Numeric bounds checks ---
        if min_value is not None:
            for value in target:
                if value < min_value:
                    raise ValueError(f"List elements must be >= {min_value}")

        if max_value is not None:
            for value in target:
                if value > max_value:
                    raise ValueError(f"List elements must be <= {max_value}")

        if value_range is not None:
            min_r, max_r = value_range
            for value in target:
                if not min_r <= value <= max_r:
                    raise ValueError(f"List elements must be within range ({min_r}, {max_r})")

        # --- Sign checks ---
        if non_negative and any(v < 0 for v in target):
            raise ValueError("All elements must be non-negative")

        if non_positive and any(v > 0 for v in target):
            raise ValueError("All elements must be non-positive")

        if non_zero and any(v == 0 for v in target):
            raise ValueError("List elements must be non-zero")

        # --- Monotonicity checks ---
        if ascending:
            for i in range(1, len(target)):
                if target[i] < target[i - 1]:
                    raise ValueError("List must be non-decreasing (ascending, equal values allowed)")

        if descending:
            for i in range(1, len(target)):
                if target[i] > target[i - 1]:
                    raise ValueError("List must be non-increasing (descending, equal values allowed)")

        if strictly_ascending:
            for i in range(1, len(target)):
                if target[i] <= target[i - 1]:
                    raise ValueError("List must be strictly ascending (no equal values)")

        if strictly_descending:
            for i in range(1, len(target)):
                if target[i] >= target[i - 1]:
                    raise ValueError("List must be strictly descending (no equal values)")

        # --- Aggregate checks ---
        if sum_range is not None:
            total = sum(target)
            min_s, max_s = sum_range
            if not min_s <= total <= max_s:
                raise ValueError(f"Sum {total} not within allowed range ({min_s}, {max_s})")

        if mean_range is not None and len(target) > 0:
            mean_value = sum(target) / len(target)
            min_m, max_m = mean_range
            if not min_m <= mean_value <= max_m:
                raise ValueError(f"Mean {mean_value} not within allowed range ({min_m}, {max_m})")

    """
    DOCCHECK TESTS:

    # --- Type / Base checks ---
    >>test: cls.validate_Numeric_List([1, 2, 3]) is None
    >>test: cls.validate_Numeric_List([1, 2.0, 3]) is None
    >>test: cls.validate_Numeric_List([-1, 2.0, -3, 0]) is None
    >>test: cls.validate_Numeric_List([1.0, 2.0, -3.0, 0]) is None
    >>error: cls.validate_Numeric_List("not a list")
    >>error: cls.validate_Numeric_List(["a", "b"])
    >>error: cls.validate_Numeric_List(["1", "23"])
    >>error: cls.validate_Numeric_List([True, False, 1])  # Bool forbidden

    # --- Length / Empty ---
    >>error: cls.validate_Numeric_List([], allowed_empty=False)
    >>test: cls.validate_Numeric_List([], allowed_empty=True) is None
    >>test: cls.validate_Numeric_List([1, 2], min_length=2) is None
    >>error: cls.validate_Numeric_List([1], min_length=2)
    >>test: cls.validate_Numeric_List([1, 2, 3], max_length=3) is None
    >>error: cls.validate_Numeric_List([1, 2, 3, 4], max_length=3)

    # --- Duplication ---
    >>error: cls.validate_Numeric_List([1, 2, 1], allow_duplication=False)
    >>test: cls.validate_Numeric_List([1, 2, 3], allow_duplication=False) is None
    >>test: cls.validate_Numeric_List([1, 1, 2], allow_duplication=True) is None

    # --- Allowed / Forbidden values ---
    >>test: cls.validate_Numeric_List([1, 2], allowed_values=[1, 2, 3]) is None
    >>error: cls.validate_Numeric_List([1, 9], allowed_values=[1, 2, 3])
    >>test: cls.validate_Numeric_List([1, 2, 3], forbidden_values=[9, 10]) is None
    >>error: cls.validate_Numeric_List([1, 2, 10], forbidden_values=[9, 10])

    # --- Numeric boundaries ---
    >>test: cls.validate_Numeric_List([5, 6, 7], min_value=5) is None
    >>error: cls.validate_Numeric_List([4, 6, 7], min_value=5)
    >>test: cls.validate_Numeric_List([1, 2, 3], max_value=3) is None
    >>error: cls.validate_Numeric_List([1, 2, 5], max_value=3)
    >>test: cls.validate_Numeric_List([3, 4, 5], value_range=(3, 5)) is None
    >>error: cls.validate_Numeric_List([2, 3, 4], value_range=(3, 5))

    # --- Sign checks ---
    >>test: cls.validate_Numeric_List([0, 1, 2], non_negative=True) is None
    >>error: cls.validate_Numeric_List([-1, 0, 1], non_negative=True)
    >>test: cls.validate_Numeric_List([-3, -2, -1], non_positive=True) is None
    >>error: cls.validate_Numeric_List([-1, 0, 1], non_positive=True)
    >>test: cls.validate_Numeric_List([1, 2, 3], non_zero=True) is None
    >>error: cls.validate_Numeric_List([0, 2, 3], non_zero=True)

    # --- Monotonicity (non-strict) ---
    >>test: cls.validate_Numeric_List([1, 1, 2, 3], ascending=True) is None
    >>error: cls.validate_Numeric_List([3, 2, 3], ascending=True)
    >>test: cls.validate_Numeric_List([3, 3, 2, 1], descending=True) is None
    >>error: cls.validate_Numeric_List([1, 3, 2], descending=True)
    >>test: cls.validate_Numeric_List([1, 2, 2.0, 3], ascending=True) is None
    >>test: cls.validate_Numeric_List([3.0, 3, 2, 2.0, 1.95], descending=True) is None

    # --- Monotonicity (strict) ---
    >>test: cls.validate_Numeric_List([1, 2, 3], strictly_ascending=True) is None
    >>error: cls.validate_Numeric_List([1, 1, 2], strictly_ascending=True)
    >>test: cls.validate_Numeric_List([3, 2, 1], strictly_descending=True) is None
    >>error: cls.validate_Numeric_List([3, 3, 1], strictly_descending=True)

    # --- Aggregates ---
    >>test: cls.validate_Numeric_List([1, 2, 3], sum_range=(6, 6)) is None
    >>error: cls.validate_Numeric_List([1, 2, 3], sum_range=(7, 10))
    >>test: cls.validate_Numeric_List([1, 2, 3], mean_range=(2, 2)) is None
    >>error: cls.validate_Numeric_List([1, 2, 3], mean_range=(3, 5))
    """

    @classmethod
    def validate_String_List(
        cls,
        target: Any,
        *,
        allowed_empty: bool = False,
        min_length: int | None = None,
        max_length: int | None = None,
        allow_duplication: bool = True,
        allowed_values: Sequence[str] | None = None,
        forbidden_values: Sequence[str] | None = None,
        str_min_length: int | None = None,
        str_max_length: int | None = None,
        range_length: tuple[int, int] | None = None,
        starts_with: str | None = None,
        does_not_start_with: str | None = None,
        ends_with: str | None = None,
        does_not_end_with: str | None = None,
        contains: str | Sequence[str] | None = None,
        allowed: Sequence[str] | None = None,
        forbidden: Sequence[str] | None = None,
        must_be_lowercase: bool = False,
        must_be_uppercase: bool = False,
        allow_alphabetic: bool = True,
        allow_numeric: bool = True,
        allow_special: bool = True,
        allow_whitespaces: bool = True,
        allow_empty: bool = False,
        no_consecutive_spaces: bool = False,
        regex: str | None = None,
        not_regex: str | None = None,
        json_safe: bool = False,
        ascii_only: bool = False,
    ) -> None:
        """Validate a list of strings.

        Performs both list-level and element-level validations.
        Each element is validated using `validate_String()` with
        the same keyword arguments provided here.

        Parameters
        ----------
        target : Any
            The object to validate, must be of type `list`.
        allowed_empty : bool
            Whether an empty list is allowed.
        min_length, max_length : int | None
            Minimum and maximum list lengths.
        allow_duplication : bool
            Whether duplicate elements are allowed.
        allowed_values, forbidden_values : Sequence[str] | None
            Optional element whitelist or blacklist.
        All other keyword arguments are forwarded to `validate_String()`.
        """

        # --- Type check ---
        if not isinstance(target, list):
            raise TypeError(f"Expected list, got {type(target).__name__}")

        # --- Empty list check ---
        if not allowed_empty and len(target) == 0:
            raise ValueError("Empty lists are not allowed")

        # --- Length checks ---
        if min_length is not None and len(target) < min_length:
            raise ValueError(f"List must contain at least {min_length} elements")

        if max_length is not None and len(target) > max_length:
            raise ValueError(f"List must contain at most {max_length} elements")

        # --- Duplication check ---
        if not allow_duplication:
            seen: set[str] = set()
            for element in target:
                if element in seen:
                    raise ValueError(f"Duplicate element '{element}' found in list")
                seen.add(element)

        # --- Allowed / Forbidden values ---
        if allowed_values is not None:
            for element in target:
                if element not in allowed_values:
                    raise ValueError(f"Element {element!r} not in allowed values: {allowed_values}")

        if forbidden_values is not None:
            for element in target:
                if element in forbidden_values:
                    raise ValueError(f"Element {element!r} is forbidden by validation rule")

        # --- Per-element validation using validate_String ---
        for index, element in enumerate(target):
            if not isinstance(element, str):
                raise TypeError(f"Element at index {index} must be str, got {type(element).__name__}")

            cls.validate_String(
                element,
                min_length=str_min_length,
                max_length=str_max_length,
                range_length=range_length,
                starts_with=starts_with,
                does_not_start_with=does_not_start_with,
                ends_with=ends_with,
                does_not_end_with=does_not_end_with,
                contains=contains,
                allowed=allowed,
                forbidden=forbidden,
                must_be_lowercase=must_be_lowercase,
                must_be_uppercase=must_be_uppercase,
                allow_alphabetic=allow_alphabetic,
                allow_numeric=allow_numeric,
                allow_special=allow_special,
                allow_whitespaces=allow_whitespaces,
                allow_empty=allow_empty,
                no_consecutive_spaces=no_consecutive_spaces,
                regex=regex,
                not_regex=not_regex,
                json_safe=json_safe,
                ascii_only=ascii_only,
            )

    """
    DOCCHECK TESTS:

    # --- Type ---
    >>test: cls.validate_String_List(["a", "b"]) is None
    >>error: cls.validate_String_List("not a list")

    # --- Empty ---
    >>error: cls.validate_String_List([], allowed_empty=False)
    >>test: cls.validate_String_List([], allowed_empty=True) is None

    # --- Length ---
    >>test: cls.validate_String_List(["a", "b"], min_length=2) is None
    >>error: cls.validate_String_List(["a"], min_length=2)
    >>test: cls.validate_String_List(["a", "b"], max_length=2) is None
    >>error: cls.validate_String_List(["a", "b", "c"], max_length=2)

    # --- Duplication ---
    >>test: cls.validate_String_List(["x", "y"], allow_duplication=False) is None
    >>error: cls.validate_String_List(["x", "x"], allow_duplication=False)

    # --- Allowed / Forbidden values ---
    >>test: cls.validate_String_List(["a", "b"], allowed_values=["a","b","c"]) is None
    >>error: cls.validate_String_List(["a", "z"], allowed_values=["a","b","c"])
    >>test: cls.validate_String_List(["a","b"], forbidden_values=["z"]) is None
    >>error: cls.validate_String_List(["a","z"], forbidden_values=["z"])

    # --- Element type ---
    >>error: cls.validate_String_List(["a", 2])

    # --- Forwarded String rules ---
    >>test: cls.validate_String_List(["hello", "world"], must_be_lowercase=True) is None
    >>error: cls.validate_String_List(["Hello"], must_be_lowercase=True)
    >>test: cls.validate_String_List(["UP", "CASE"], must_be_uppercase=True) is None
    >>error: cls.validate_String_List(["Up"], must_be_uppercase=True)
    >>test: cls.validate_String_List(["a_b", "a_b_c"], contains="_") is None
    >>error: cls.validate_String_List(["abc"], contains="_")
    >>test: cls.validate_String_List(["data_1", "data_2"], regex="^[a-z_\\d]+$") is None
    >>error: cls.validate_String_List(["Data_1"], regex="^[a-z_\\d]+$")
    >>test: cls.validate_String_List(["safe"], forbidden=["danger","alert"]) is None
    >>error: cls.validate_String_List(["alert"], forbidden=["danger","alert"])
    >>test: cls.validate_String_List(["ascii", "only"], ascii_only=True) is None
    >>error: cls.validate_String_List(["café"], ascii_only=True)
    """
