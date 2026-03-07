# ========== Imports ========== #

import pytest
from decimal import Decimal
from unittest.mock import MagicMock
from app.other.history import LoggingObserver, AutosaveObserver
from app.calculator.calculation import Calculation

# ========== Fixtures ========== #

@pytest.fixture
def calc_mock():
    c = Calculation("Addition", Decimal("1"), Decimal("2"))
    return c

@pytest.fixture
def calculator_mock():
    mock = MagicMock()
    mock.config.auto_save = True
    return mock

# ========== LoggingObserver Tests ========== #

def test_logging_observer(calc_mock, caplog):
    observer = LoggingObserver()
    import logging
    with caplog.at_level(logging.INFO):
        observer.update(calc_mock)
    assert "Calculation performed" in caplog.text

def test_logging_observer_none():
    observer = LoggingObserver()
    with pytest.raises(AttributeError):
        observer.update(None)

# ========== AutosaveObserver Tests ========== #

def test_autosave_init(calculator_mock):
    observer = AutosaveObserver(calculator_mock)
    assert observer.calculator is calculator_mock

def test_autosave_init_invalid():
    with pytest.raises(TypeError):
        AutosaveObserver("not a calculator")

def test_autosave_update(calculator_mock, calc_mock):
    observer = AutosaveObserver(calculator_mock)
    observer.update(calc_mock)
    calculator_mock.save_history.assert_called_once()

def test_autosave_update_no_autosave(calculator_mock, calc_mock):
    calculator_mock.config.auto_save = False
    observer = AutosaveObserver(calculator_mock)
    observer.update(calc_mock)
    calculator_mock.save_history.assert_not_called()

def test_autosave_update_none(calculator_mock):
    observer = AutosaveObserver(calculator_mock)
    with pytest.raises(AttributeError):
        observer.update(None)
