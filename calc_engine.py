import math


def evaluate_expression(expr: str) -> float:
    """Evaluate a calculator expression using the :mod:`math` library."""
    expression = expr
    expression = expression.replace('sin(', 'math.sin(math.radians(')
    expression = expression.replace('cos(', 'math.cos(math.radians(')
    expression = expression.replace('tan(', 'math.tan(math.radians(')
    expression = expression.replace('log10(', 'math.log10(')
    expression = expression.replace('log(', 'math.log(')
    return eval(expression)
