
# ========== Imports ========== #

from abc import ABC, abstractmethod
from typing import Any
import logging
from app.calculator.calculation import Calculation

# ======================================== #

# History Observer base class
class HistoryObserver(ABC):
    """
    Observer that monitors & reacts to new calculation events.
    """
    from app.calculator.calculation import Calculation

    @abstractmethod
    def update(self, calculation) -> None:
        """Handles new calculation events"""
        pass # pragma: no cover


# Logging subclass
class LoggingObserver(HistoryObserver):
    """
    Listens for new calculations and logs their details to a designated file.
    """

    def update(self, calculation) -> None:
        """Log new calculations"""
        if calculation is None:
            raise AttributeError("Calculation cannot be none")
        logging.info(
            f"Calculation performed: {calculation.operation}"
            f"({calculation.operand1}, {calculation.operand2}) ="
            f"{calculation.result}"
        )

# Autosave subclass
class AutosaveObserver(HistoryObserver):
    """
    Listens for new calculations then saves them.
    """
    

    def __init__(self, calculator: Any):
        """Initialize AutosaveObserver"""

        if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):
            raise TypeError("Calculator must have 'config' and 'save_history' attributes")
        self.calculator = calculator

    def update(self, calculation) -> None:
        """Saves calculation whenever a new calculation is performed"""
        from app.calculator.calculation import Calculation

        if calculation is None:
            raise AttributeError("Calculation can't be None:")
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved")