# ========== Imports ========== #

import pytest
import pandas as pd
from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock

from app.calculator.calculator import Calculator
from app.calculator.operations import Addition, Division
from app.other.exceptions import OperationError, ValidationError
from app.other.history import HistoryObserver
from app.config.config import Config

# ========== Fixtures ========== #

@pytest.fixture
def calc(tmp_path):
    config = Config(base_dir=tmp_path)
    return Calculator(config=config)

# ========== Init Tests ========== #

def test_calculator_init(calc):
    assert calc.history == []
    assert calc.operation_strategy is None
    assert calc.undo_stack == []
    assert calc.redo_stack == []

def test_calculator_default_config():
    c = Calculator()
    assert c.config is not None

# ========== Operation Tests ========== #

def test_set_operation(calc):
    op = Addition()
    calc.set_operation(op)
    assert calc.operation_strategy is op

def test_perform_operation(calc):
    calc.set_operation(Addition())
    result = calc.perform_operation("2", "3")
    assert result == Decimal("5")

def test_perform_no_operation_set(calc):
    with pytest.raises(OperationError, match="No operation set"):
        calc.perform_operation("1", "2")

def test_perform_validation_error(calc):
    calc.set_operation(Addition())
    with pytest.raises(ValidationError):
        calc.perform_operation("abc", "2")

def test_perform_operation_error(calc):
    calc.set_operation(Division())
    with pytest.raises((ValidationError, OperationError)):
        calc.perform_operation("1", "0")

# ========== History Tests ========== #

def test_show_history_empty(calc):
    assert calc.show_history() == []

def test_show_history_after_op(calc):
    calc.set_operation(Addition())
    calc.perform_operation("1", "2")
    history = calc.show_history()
    assert len(history) == 1
    assert "Addition" in history[0]

def test_clear_history(calc):
    calc.set_operation(Addition())
    calc.perform_operation("1", "2")
    calc.clear_history()
    assert calc.history == []
    assert calc.undo_stack == []
    assert calc.redo_stack == []

def test_history_max_size(calc):
    calc.config.max_history_size = 2
    calc.set_operation(Addition())
    calc.perform_operation("1", "1")
    calc.perform_operation("2", "2")
    calc.perform_operation("3", "3")
    assert len(calc.history) == 2

def test_get_history_dataframe(calc):
    calc.set_operation(Addition())
    calc.perform_operation("1", "2")
    df = calc.get_history_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1

# ========== Save/Load Tests ========== #

def test_save_and_load_history(calc):
    calc.set_operation(Addition())
    calc.perform_operation("5", "10")
    calc.save_history()
    calc.clear_history()
    assert calc.history == []
    calc.load_history()
    assert len(calc.history) == 1

def test_save_empty_history(calc):
    calc.save_history()
    assert calc.config.history_file.exists()

def test_load_no_file(calc):
    if calc.config.history_file.exists():
        calc.config.history_file.unlink()
    calc.load_history()
    assert calc.history == []

# ========== Undo/Redo Tests ========== #

def test_undo(calc):
    calc.set_operation(Addition())
    calc.perform_operation("1", "2")
    assert len(calc.history) == 1
    assert calc.undo() is True
    assert calc.history == []

def test_undo_empty(calc):
    assert calc.undo() is False

def test_redo(calc):
    calc.set_operation(Addition())
    calc.perform_operation("1", "2")
    calc.undo()
    assert calc.redo() is True
    assert len(calc.history) == 1

def test_redo_empty(calc):
    assert calc.redo() is False

# ========== Observer Tests ========== #

def test_add_observer(calc):
    observer = MagicMock(spec=HistoryObserver)
    calc.add_observer(observer)
    assert observer in calc.observers

def test_remove_observer(calc):
    observer = MagicMock(spec=HistoryObserver)
    calc.add_observer(observer)
    calc.remove_observer(observer)
    assert observer not in calc.observers

def test_notify_observers(calc):
    observer = MagicMock(spec=HistoryObserver)
    calc.add_observer(observer)
    calc.set_operation(Addition())
    calc.perform_operation("1", "2")
    observer.update.assert_called_once()
