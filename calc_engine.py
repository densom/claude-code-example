import math


def evaluate_expression(expr: str) -> float:
    """Evaluate a calculator expression using the :mod:`math` library."""
    expression = expr

    # Replace trigonometric function names with degree-based helpers
    expression = expression.replace("sin(", "sin_deg(")
    expression = expression.replace("cos(", "cos_deg(")
    expression = expression.replace("tan(", "tan_deg(")

    allowed = {
        "sin_deg": lambda x: math.sin(math.radians(x)),
        "cos_deg": lambda x: math.cos(math.radians(x)),
        "tan_deg": lambda x: math.tan(math.radians(x)),
        "log10": math.log10,
        "log": math.log,
        "pi": math.pi,
        "e": math.e,
        "math": math,
    }

    return eval(expression, {"__builtins__": {}}, allowed)
