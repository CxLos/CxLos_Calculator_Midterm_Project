# ========== Imports ========== #

import pytest
from unittest.mock import patch, MagicMock
from app.calculator.repl import repl

# ========== Helpers ========== #

def run_repl(inputs):
    """Run repl with a list of simulated user inputs."""
    with patch('builtins.input', side_effect=inputs):
        repl()

# ========== Tests ========== #

def test_exit(capsys):
    run_repl(["exit"])
    out = capsys.readouterr().out
    assert "Goodbye!" in out

def test_help(capsys):
    run_repl(["help", "exit"])
    out = capsys.readouterr().out
    assert "Available commands" in out

def test_add(capsys):
    run_repl(["add", "2", "3", "exit"])
    out = capsys.readouterr().out
    assert "5" in out

def test_subtract(capsys):
    run_repl(["subtract", "10", "4", "exit"])
    out = capsys.readouterr().out
    assert "6" in out

def test_multiply(capsys):
    run_repl(["multiply", "3", "5", "exit"])
    out = capsys.readouterr().out
    assert "15" in out

def test_divide(capsys):
    run_repl(["divide", "10", "2", "exit"])
    out = capsys.readouterr().out
    assert "5" in out

def test_history_empty(capsys):
    run_repl(["clear", "history", "exit"])
    out = capsys.readouterr().out
    assert "No history yet" in out

def test_history_with_entries(capsys):
    run_repl(["add", "1", "2", "history", "exit"])
    out = capsys.readouterr().out
    assert "Calculation History" in out

def test_clear(capsys):
    run_repl(["add", "1", "2", "clear", "exit"])
    out = capsys.readouterr().out
    assert "History cleared" in out

def test_undo(capsys):
    run_repl(["add", "1", "2", "undo", "exit"])
    out = capsys.readouterr().out
    assert "Operation undone" in out

def test_undo_empty(capsys):
    run_repl(["undo", "exit"])
    out = capsys.readouterr().out
    assert "Nothing to undo" in out

def test_redo(capsys):
    run_repl(["add", "1", "2", "undo", "redo", "exit"])
    out = capsys.readouterr().out
    assert "Operation redone" in out

def test_redo_empty(capsys):
    run_repl(["redo", "exit"])
    out = capsys.readouterr().out
    assert "Nothing to redo" in out

def test_save(capsys):
    run_repl(["save", "exit"])
    out = capsys.readouterr().out
    assert "History saved successfully" in out

def test_load(capsys):
    run_repl(["add", "1", "2", "save", "load", "exit"])
    out = capsys.readouterr().out
    assert "History loaded successfully" in out

def test_cancel_first_number(capsys):
    run_repl(["add", "cancel", "exit"])
    out = capsys.readouterr().out
    assert "Operation canceled" in out

def test_cancel_second_number(capsys):
    run_repl(["add", "5", "cancel", "exit"])
    out = capsys.readouterr().out
    assert "Operation canceled" in out

def test_validation_error(capsys):
    run_repl(["divide", "1", "0", "exit"])
    out = capsys.readouterr().out
    assert "Error:" in out

def test_invalid_input(capsys):
    run_repl(["add", "abc", "2", "exit"])
    out = capsys.readouterr().out
    assert "Error:" in out

def test_unknown_command(capsys):
    run_repl(["foobar", "exit"])
    out = capsys.readouterr().out
    assert "Unknown command" in out

def test_eof(capsys):
    with patch('builtins.input', side_effect=EOFError):
        repl()
    out = capsys.readouterr().out
    assert "Input terminated" in out

def test_keyboard_interrupt(capsys):
    with patch('builtins.input', side_effect=[KeyboardInterrupt, "exit"]):
        repl()
    out = capsys.readouterr().out
    assert "Operation cancelled" in out