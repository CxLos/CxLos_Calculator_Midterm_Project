# ========== Imports ========== #

import pytest
from decimal import Decimal
from app.other.validator import InputValidator
from app.other.exceptions import ValidationError
from app.config.config import Config

# ========== Tests ========== #

@pytest.fixture
def config():
    return Config()

def test_validate_integer(config):
    assert InputValidator.validate_number(5, config) == Decimal("5")

def test_validate_string(config):
    assert InputValidator.validate_number("  3.14  ", config) == Decimal("3.14")

def test_validate_decimal(config):
    assert InputValidator.validate_number(Decimal("2.5"), config) == Decimal("2.5")

def test_validate_invalid_format(config):
    with pytest.raises(ValidationError, match="Invalid number format"):
        InputValidator.validate_number("abc", config)

def test_validate_exceeds_max(config):
    config.max_input_value = Decimal("100")
    with pytest.raises(ValidationError, match="Value exceeds maximum"):
        InputValidator.validate_number("999", config)
