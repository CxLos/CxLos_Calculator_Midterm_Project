# ========== Imports ========== #

import pytest
from decimal import Decimal
from typing import Any, Dict, Type

from app.other.exceptions import ValidationError
from app.calculator.operations import (
    Operation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    SQRT,
    Modulus,
    Floor,
    Percentage,
    OperationFactory,
)

# ========== Operation Tests ========== #

def test_addition():
    assert Addition().execute(Decimal("2"), Decimal("3")) == Decimal("5")

def test_subtraction():
    assert Subtraction().execute(Decimal("10"), Decimal("4")) == Decimal("6")

def test_multiplication():
    assert Multiplication().execute(Decimal("3"), Decimal("5")) == Decimal("15")

def test_division():
    assert Division().execute(Decimal("10"), Decimal("2")) == Decimal("5")

def test_division_by_zero():
    with pytest.raises(ValidationError):
        Division().execute(Decimal("10"), Decimal("0"))

def test_power():
    assert Power().execute(Decimal("2"), Decimal("3")) == Decimal("8")

def test_sqrt():
    assert SQRT().execute(Decimal("9"), Decimal("2")) == Decimal(pow(9, 0.5))

def test_modulus():
    assert Modulus().execute(Decimal("10"), Decimal("3")) == Decimal(10 % 3)

def test_floor():
    assert Floor().execute(Decimal("10"), Decimal("3")) == Decimal("3")

def test_percentage():
    assert Percentage().execute(Decimal("200"), Decimal("10")) == Decimal("20")

# ========== Factory Tests ========== #

def test_factory_create():
    op = OperationFactory.create_operation("add")
    assert isinstance(op, Addition)

def test_factory_unknown():
    with pytest.raises(ValueError):
        OperationFactory.create_operation("unknown")

def test_factory_register():
    OperationFactory.register_operation("add2", Addition)
    op = OperationFactory.create_operation("add2")
    assert isinstance(op, Addition)

def test_factory_register_invalid():
    with pytest.raises(TypeError):
        OperationFactory.register_operation("bad", str)

# ========== Validation Tests ========== #

def test_operation_str():
    assert str(Addition()) == "Addition"

def test_power_negative_exponent():
    with pytest.raises(ValidationError):
        Power().execute(Decimal("2"), Decimal("-1"))

def test_sqrt_negative_number():
    with pytest.raises(ValidationError):
        SQRT().execute(Decimal("-4"), Decimal("2"))

def test_sqrt_zero_root():
    with pytest.raises(ValidationError):
        SQRT().execute(Decimal("4"), Decimal("0"))

def test_modulus_by_zero():
    with pytest.raises(ValidationError):
        Modulus().execute(Decimal("10"), Decimal("0"))

def test_floor_by_zero():
    with pytest.raises(ValidationError):
        Floor().execute(Decimal("10"), Decimal("0"))