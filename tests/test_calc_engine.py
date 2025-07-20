import math
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from calc_engine import evaluate_expression


def test_basic_arithmetic():
    expr = "2+3*4-5/2"
    assert math.isclose(evaluate_expression(expr), 2 + 3*4 - 5/2)

def test_trigonometric_functions():
    assert math.isclose(evaluate_expression("sin(30)"), 0.5, rel_tol=1e-9)
    assert math.isclose(evaluate_expression("cos(60)"), 0.5, rel_tol=1e-9)
    assert math.isclose(evaluate_expression("tan(45)"), 1.0, rel_tol=1e-9)

def test_logarithms():
    assert math.isclose(evaluate_expression("log10(1000)"), 3.0, rel_tol=1e-9)
    assert math.isclose(evaluate_expression("log(math.e)"), 1.0, rel_tol=1e-9)

def test_exponentiation_and_negatives():
    assert evaluate_expression("2**3") == 8
    assert evaluate_expression("(-3)**2") == 9

def test_zero_division_error():
    with pytest.raises(ZeroDivisionError):
        evaluate_expression("1/0")
