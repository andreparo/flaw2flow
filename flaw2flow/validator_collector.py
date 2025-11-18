import ast
from typing import Any


class ValidatorCollector(ast.NodeVisitor):
    """
    AST visitor that scans a specific function body and collects all calls to
    F2F.validate_* along with the parameter names they are applied to.

    It works by:
    - Entering only the target function (matching its name)
    - Traversing nested structures inside that function (including inner defs)
    - Detecting calls of the form:
          F2F.validate_Xxx(param)
          F2F.validate_Xxx(target=param)
    - Recording for each parameter the set of validator names used.

    Attributes
    ----------
    target_func_name : str
        Name of the function we want to analyze.
    in_target : bool
        Whether the visitor is currently inside the target function's body.
    result : dict[str, set[str]]
        Mapping: parameter name → set of F2F.validate_* method names found.
    """

    def __init__(self, target_func_name: str) -> None:
        """
        Initialize the visitor.

        Parameters
        ----------
        target_func_name : str
            The function name where validation calls will be collected.
        """
        self.target_func_name = target_func_name
        self.in_target = False
        self.result: dict[str, set[str]] = {}

    def visit_Function_Def(self, node: ast.FunctionDef) -> Any:
        """
        Visit a regular function definition.

        Behavior:
        - When encountering the target function name, switch into "in_target" mode
          and traverse its body.
        - When already inside the target function, still visit nested definitions.
        - Other functions at the same level are ignored.

        Parameters
        ----------
        node : ast.FunctionDef
            The function definition AST node.
        """
        if node.name == self.target_func_name and not self.in_target:
            # Enter the target function
            self.in_target = True
            self.generic_visit(node)
            self.in_target = False
        elif self.in_target:
            # Nested function: still traverse to catch validations inside
            self.generic_visit(node)

    def visit_Async_Function_Def(self, node: ast.AsyncFunctionDef) -> Any:
        """
        Visit an async function definition.

        Uses the same logic as visit_FunctionDef so that async functions can be
        validated exactly the same way.

        Parameters
        ----------
        node : ast.AsyncFunctionDef
            The async function definition AST node.
        """
        if node.name == self.target_func_name and not self.in_target:
            self.in_target = True
            self.generic_visit(node)
            self.in_target = False
        elif self.in_target:
            self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        """
        Visit a function/method call.

        When inside the target function, this detects calls of the form:

            F2F.validate_Xxx(arg)
            F2F.validate_Xxx(target=arg)

        and records the validator name for the corresponding parameter.

        Parameters
        ----------
        node : ast.Call
            The call AST node.
        """
        if not self.in_target:
            return

        # Look for F2F.validate_* calls
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if node.func.value.id == "F2F" and node.func.attr.startswith("validate_"):
                validator_name = node.func.attr
                param_names: set[str] = set()

                # First positional arg: F2F.validate_Xxx(x)
                if node.args:
                    first = node.args[0]
                    if isinstance(first, ast.Name):
                        param_names.add(first.id)

                # Keyword target=... : F2F.validate_Xxx(target=x)
                for kw in node.keywords:
                    if kw.arg == "target" and isinstance(kw.value, ast.Name):
                        param_names.add(kw.value.id)

                # Store in results
                for pname in param_names:
                    if pname not in self.result:
                        self.result[pname] = set()
                    self.result[pname].add(validator_name)

        # Continue scanning
        self.generic_visit(node)
