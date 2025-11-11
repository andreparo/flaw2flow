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
