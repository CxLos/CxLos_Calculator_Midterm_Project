# ========== Imports ========== #

import pytest
from decimal import Decimal
from app.calculator.calculation import Calculation
from app.other.exceptions import OperationError

# ========== Calculate Tests ========== #

def test_addition():
    c = Calculation("Addition", Decimal("2"), Decimal("3"))
    assert c.result == Decimal("5")

def test_subtraction():
    c = Calculation("Subtraction", Decimal("5"), Decimal("3"))
    assert c.result == Decimal("2")

def test_multiplication():
    c = Calculation("Multiplication", Decimal("4"), Decimal("3"))
    assert c.result == Decimal("12")

def test_division():
    c = Calculation("Division", Decimal("10"), Decimal("2"))
    assert c.result == Decimal("5")

def test_power():
    c = Calculation("Power", Decimal("2"), Decimal("3"))
    assert c.result == Decimal("8")

def test_sqrt():
    c = Calculation("SQRT", Decimal("9"), Decimal("2"))
    assert float(c.result) == pytest.approx(3.0)

def test_modulus():
    c = Calculation("Modulus", Decimal("10"), Decimal("3"))
    assert c.result == Decimal("1")

def test_floor():
    c = Calculation("Floor", Decimal("10"), Decimal("3"))
    assert c.result == Decimal("3")

def test_percentage():
    c = Calculation("Percentage", Decimal("200"), Decimal("10"))
    assert c.result == Decimal("20")

def test_unknown_operation():
    with pytest.raises(OperationError, match="Unknow operation"):
        Calculation("BadOp", Decimal("1"), Decimal("2"))

# ========== to_dict / from_dict Tests ========== #

def test_to_dict():
    c = Calculation("Addition", Decimal("1"), Decimal("2"))
    d = c.to_dict()
    assert d["operation"] == "Addition"
    assert d["operand1"] == "1"
    assert d["operand2"] == "2"
    assert d["result"] == "3"
    assert "timestamp" in d

def test_from_dict():
    c = Calculation("Addition", Decimal("1"), Decimal("2"))
    d = c.to_dict()
    c2 = Calculation.from_dict(d)
    assert c2.result == Decimal("3")
    assert c2.operation == "Addition"

def test_from_dict_invalid():
    with pytest.raises(OperationError, match="Invalid calculation data"):
        Calculation.from_dict({"operation": "Addition"})

# ========== str / repr / eq Tests ========== #

def test_str():
    c = Calculation("Addition", Decimal("1"), Decimal("2"))
    assert str(c) == "Addition(1, 2) = 3"

def test_repr():
    c = Calculation("Addition", Decimal("1"), Decimal("2"))
    r = repr(c)
    assert "Calculation(operation='Addition'" in r

def test_eq():
    c1 = Calculation("Addition", Decimal("1"), Decimal("2"))
    c2 = Calculation("Addition", Decimal("1"), Decimal("2"))
    assert c1 == c2

def test_eq_not_implemented():
    c = Calculation("Addition", Decimal("1"), Decimal("2"))
    assert c.__eq__("not a calc") is NotImplemented

# ========== format_result Test ========== #

def test_format_result():
    c = Calculation("Division", Decimal("10"), Decimal("3"))
    result = c.format_result(4)
    assert "." in result
