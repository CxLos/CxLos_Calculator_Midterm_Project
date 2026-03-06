
# ========== Imports =========== #

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any
from app.other.exceptions import ValidationError
from app.config.config import Config

@dataclass
class InputValidator:
    """Validate calculator inputs"""
    
    @staticmethod
    def validate_number(value: Any, config: Config) -> Decimal:
        """
        Validate and convert to proper format
        """
        try:
            if isinstance(value, str):
                value = value.strip()
            number = Decimal(str(value))
            if abs(number) > config.max_input_value:
                raise ValidationError(f"Value exceeds maximum allowed: {config.max_input_value}")
            return number.normalize()
        except InvalidOperation as e:
            raise ValidationError(f"Invalid number format: {value}") from e
