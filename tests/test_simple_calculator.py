
import pytest
from src.utils.simple_calculator import Calculator

def test_calculator_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5

def test_calculator_subtract():
    calc = Calculator()
    assert calc.subtract(5, 2) == 3

def test_calculator_multiply():
    calc = Calculator()
    assert calc.multiply(4, 3) == 12

def test_calculator_divide():
    calc = Calculator()
    assert calc.divide(10, 2) == 5.0
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)