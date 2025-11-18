import ast
import inspect
import types
from typing import Any, get_type_hints, get_origin, get_args
import os
import importlib.util
from types import ModuleType


class F2FGuard:
    """
    Performs validation coverage checks for functions and classes.

    Uses AST to verify that every parameter with a builtin type annotation
    is validated with the corresponding F2F.validate_* call.

    Supported builtin → validator:
        int           → validate_Int
        float         → validate_Float
        bool          → validate_Bool
        str           → validate_String
        bytes         → validate_Bytes
        dict[...]     → validate_Dict
        tuple[...]    → validate_Tuple
        list[int]     → validate_Numeric_List
        list[float]   → validate_Numeric_List
        list[str]     → validate_String_List
        list[Other]   → validate_List

    Union rules:
        int | str   → both validators required
        int | None  → only validate_Int required
    """

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    @classmethod
    def validate_Function(cls, func: Any) -> None:
        """Validate a function or method according to F2F rules."""

        if not inspect.isfunction(func) and not inspect.ismethod(func):
            raise TypeError(f"validate_Function expects a function/method, got {type(func).__name__}")

        # Retrieve module file path injected during import
        module_globals = func.__globals__  # type: ignore
        if "__f2f_path__" not in module_globals:
            raise RuntimeError("Module missing __f2f_path__; use F2FGuard._import_From_Path")

        source_path = module_globals["__f2f_path__"]

        # Extract type hints
        sig = inspect.signature(func)
        try:
            type_hints = get_type_hints(func, include_extras=True)
        except Exception:
            type_hints = getattr(func, "__annotations__", {}) or {}

        param_required: dict[str, set[str]] = {}

        # Determine required validators based on type annotations
        for name, param in sig.parameters.items():

            # Skip self/cls
            if name in ("self", "cls"):
                continue

            # Skip *args/**kwargs
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue

            annotation = type_hints.get(name, inspect._empty)

            if annotation is inspect._empty:
                raise TypeError(
                    f"Parameter '{name}' of function '{func.__qualname__}' " "has no type annotation but F2FGuard requires it."
                )

            needed = cls._required_Validators_For_Annotation(annotation)
            if needed:
                param_required[name] = needed

        # Collect validators used inside function body
        param_actual = cls._collect_F2f_Validations(func, source_path)

        # Compare required vs actual
        for pname, required_set in param_required.items():
            actual_set = param_actual.get(pname, set())

            missing = required_set - actual_set
            if missing:
                raise ValueError(f"Function '{func.__qualname__}': parameter '{pname}' " f"is missing validator(s): {sorted(missing)}")

            extra = actual_set - required_set
            if extra:
                raise ValueError(
                    f"Function '{func.__qualname__}': parameter '{pname}' " f"has unexpected validator(s): {sorted(extra)}"
                )

    @classmethod
    def validate_Project(cls, module: Any) -> None:
        """Validate all functions and constructors in a module."""

        if module is None or not hasattr(module, "__name__"):
            raise TypeError(f"validate_Project expects a module/package object, got {type(module).__name__}")

        module_name = module.__name__

        # Top-level functions
        for name, obj in vars(module).items():
            if inspect.isfunction(obj) and obj.__module__ == module_name:
                cls.validate_Function(obj)

        # Constructors (__init__)
        for name, obj in vars(module).items():
            if inspect.isclass(obj) and obj.__module__ == module_name:
                init = getattr(obj, "__init__", None)
                if inspect.isfunction(init) or inspect.ismethod(init):
                    cls.validate_Function(init)

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #

    @classmethod
    def _required_Validators_For_Annotation(cls, annotation: Any) -> set[str]:
        """Return the set of required validators for a type annotation."""
        from typing import Union

        required = set()
        origin = get_origin(annotation)
        args = get_args(annotation)

        # Handle Union[A, B] and A | B
        if origin is Union or isinstance(annotation, types.UnionType):
            for arg in args:
                if arg is type(None):
                    continue
                required |= cls._required_Validators_For_Annotation(arg)
            return required

        # Builtins
        if annotation is int:
            return {"validate_Int"}
        if annotation is float:
            return {"validate_Float"}
        if annotation is bool:
            return {"validate_Bool"}
        if annotation is str:
            return {"validate_String"}
        if annotation is bytes:
            return {"validate_Bytes"}

        # Containers
        if origin is list or annotation is list:
            if args:
                elem = args[0]
                if elem in (int, float):
                    return {"validate_Numeric_List"}
                if elem is str:
                    return {"validate_String_List"}
                return {"validate_List"}
            return {"validate_List"}

        if origin is dict or annotation is dict:
            return {"validate_Dict"}

        if origin is tuple or annotation is tuple:
            return {"validate_Tuple"}

        return set()  # unsupported/custom type

    # ------- AST collection of F2F.validate_* calls ------------------- #

    @classmethod
    def _collect_F2f_Validations(cls, func: Any, source_path: str) -> dict[str, set[str]]:
        """
        Parse the REAL source file and gather F2F.validate_* calls
        only inside the specific function/method `func`.
        """

        try:
            with open(source_path, "r", encoding="utf-8") as f:
                source = f.read()
        except Exception as e:
            raise RuntimeError(f"Could not read source file '{source_path}': {e}")

        tree = ast.parse(source)
        func_name = func.__name__
        func_lineno = func.__code__.co_firstlineno

        # Find the matching FunctionDef or AsyncFunctionDef node
        target_node: ast.AST | None = None
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name == func_name:
                    # Prefer exact lineno match if possible
                    if getattr(node, "lineno", None) == func_lineno:
                        target_node = node
                        break
                    # Fallback: first function with this name
                    if target_node is None:
                        target_node = node

        if target_node is None:
            raise RuntimeError(f"Function '{func_name}' not found in AST for file '{source_path}'")

        class SimpleValidatorCollector(ast.NodeVisitor):
            """
            Collects all `F2F.validate_*` calls inside a *single* function AST node.

            The collector builds a mapping:

                {
                    "<parameter_name>": { "validate_Int", "validate_String", ... }
                }

            This lets F2FGuard compare:
                • which validators SHOULD be present (from type annotations)
                • which validators ARE present (collected by this class)

            The collector recognizes calls like:

                F2F.validate_Int(x)
                F2F.validate_String(name)
                F2F.validate_List(items)

            both in positional form:

                F2F.validate_Int(x)

            and keyword form:

                F2F.validate_Int(x=x)

            Only direct variable references (ast.Name) are supported, exactly as required
            by the F2F validation rules.
            """

            def __init__(self) -> None:
                """
                Initialize the validator collector.

                Attributes
                ----------
                result : dict[str, set[str]]
                    Dictionary mapping parameter names to the set of validator names
                    applied to them. For example:

                        {
                            "x": {"validate_Int"},
                            "name": {"validate_String"},
                        }
                """
                self.result: dict[str, set[str]] = {}

            def _record(self, param_name: str, validator: str) -> None:
                """
                Record that a specific validator was applied to a specific parameter.

                Parameters
                ----------
                param_name : str
                    The function parameter name being validated.
                validator : str
                    The validator function name (e.g., 'validate_Int').

                Notes
                -----
                This method ensures:
                    • result[param_name] exists
                    • validator is added to its set
                """
                if param_name not in self.result:
                    self.result[param_name] = set()
                self.result[param_name].add(validator)

            def visit_Call(self, node: ast.Call) -> Any:
                """
                Process each function call in the AST to detect validator usage.

                This method identifies calls of the form:
                    F2F.validate_*(...)

                The algorithm checks:

                1. The function being called is:
                    F2F.validate_<Type>
                i.e. an ast.Attribute node where:
                    • base is Name(id="F2F")
                    • attr starts with "validate_"

                2. Extract validator name:
                    validate_Int
                    validate_String
                    validate_Tuple
                    ...

                3. Map validators to parameters by:
                    a. Positional argument:
                        F2F.validate_Int(x)
                    → arg0 must be ast.Name → "x"

                    b. Keyword argument:
                        F2F.validate_Int(x=x)
                    → kw.value must be ast.Name → "x"

                4. Store the mapping via self._record().

                Parameters
                ----------
                node : ast.Call
                    The AST node representing a function call.

                Returns
                -------
                Any
                    Always returns None; traversal continues.

                Notes
                -----
                After analyzing the call, this method continues traversing the AST
                by calling `self.generic_visit(node)` so nested validators are also detected.
                """
                validator_name: str | None = None

                # Detect F2F.validate_*(...)
                if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                    if node.func.value.id == "F2F" and node.func.attr.startswith("validate_"):
                        validator_name = node.func.attr

                if validator_name:
                    # Positional first argument: F2F.validate_Int(x)
                    if node.args:
                        arg0 = node.args[0]
                        if isinstance(arg0, ast.Name):
                            self._record(arg0.id, validator_name)

                    # Keyword style: F2F.validate_Int(x=x)
                    for kw in node.keywords:
                        if kw.arg is not None and isinstance(kw.value, ast.Name):
                            self._record(kw.value.id, validator_name)

                # Continue walking children
                self.generic_visit(node)

        collector = SimpleValidatorCollector()
        collector.visit(target_node)
        return collector.result

    # ------------------------------------------------------------------ #
    # Package / file helpers
    # ------------------------------------------------------------------ #

    @classmethod
    def validate_Package(cls, path: str) -> None:
        """Validate a package or single .py file."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path not found: {path}")

        if os.path.isfile(path):
            cls.validate_File(path)
            return

        for root, _, files in os.walk(path):
            for fname in files:
                if fname.endswith(".py"):
                    cls.validate_File(os.path.join(root, fname))

    @staticmethod
    def _import_From_Path(path: str) -> ModuleType:
        """Import a module from a file path and store the path in globals."""
        module_name = os.path.splitext(os.path.basename(path))[0] + "__f2fguard__"

        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Unable to load module from: {path}")

        module = importlib.util.module_from_spec(spec)

        # Attach the path safely in module's globals so validate_Function can find it
        module.__dict__["__f2f_path__"] = path

        spec.loader.exec_module(module)
        return module

    @classmethod
    def validate_File(cls, path: str) -> None:
        """Validate a single Python file."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        if not path.endswith(".py"):
            raise ValueError(f"Expected a .py file, got: {path}")

        module = cls._import_From_Path(path)
        cls.validate_Project(module)

    """
    DOCHECK

    >>test: F2FGuard.validate_File("flaw2flow/sandbox/ok_bool_validated.py") is None

    >>error: F2FGuard.validate_File("flaw2flow/sandbox/constructor_missing_validation.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/miss_bool_validation.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/miss_bytes_validation.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/miss_dict_validation.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/miss_float_validation.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/miss_list_validation.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/miss_numeric_list_validation.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/miss_string_list_validation.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/miss_string_validation.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/miss_tuple_validation.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/miss_union_complex_member.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/miss_union_member.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/miss_validation_int.py")

    >>test: F2FGuard.validate_File("flaw2flow/sandbox/ok_bytes_validated.py") is None
    >>test: F2FGuard.validate_File("flaw2flow/sandbox/ok_constructor_validated.py") is None
    >>test: F2FGuard.validate_File("flaw2flow/sandbox/ok_dict_validated.py") is None
    >>test: F2FGuard.validate_File("flaw2flow/sandbox/ok_float_validated.py") is None
    >>test: F2FGuard.validate_File("flaw2flow/sandbox/ok_list_numeric.py") is None
    >>test: F2FGuard.validate_File("flaw2flow/sandbox/ok_list_validated.py") is None
    >>test: F2FGuard.validate_File("flaw2flow/sandbox/ok_simple_int.py") is None
    >>test: F2FGuard.validate_File("flaw2flow/sandbox/ok_string_list_validated.py") is None
    >>test: F2FGuard.validate_File("flaw2flow/sandbox/ok_string_validated.py") is None
    >>test: F2FGuard.validate_File("flaw2flow/sandbox/ok_tuple_validated.py") is None
    >>test: F2FGuard.validate_File("flaw2flow/sandbox/ok_union_complex.py") is None
    >>test: F2FGuard.validate_File("flaw2flow/sandbox/ok_union_int_str.py") is None

    >>error: F2FGuard.validate_File("flaw2flow/sandbox/wrong_bool_validator.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/wrong_bytes_validator.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/wrong_dict_validator.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/wrong_float_validator.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/wrong_list_string.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/wrong_list_validator.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/wrong_numeric_list_validator.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/wrong_string_list_validator.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/wrong_string_validator.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/wrong_tuple_validator.py")
    >>error: F2FGuard.validate_File("flaw2flow/sandbox/wrong_validation_int.py")

    """
