
# ============= Imports ============= #

from app.other.exceptions import ValidationError
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict

# =================================== #

# Base Class
class Operation(ABC):
    """
    Operations Base Class
    """

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Performs specified operation
        """
        pass  # pragma: no cover

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operation before execution
        """
        pass

    def __str__(self) -> str:
        """
        Returns operation as a string
        """
        return self.__class__.__name__

# Addition Operation
class Addition(Operation):
    """
    Adds 2 numbers
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute addition
        """
        self.validate_operands(a, b)
        return a + b

# Subtraction Operation
class Subtraction(Operation):
    """
    Subtracts 2 numbers
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        execute subtraction
        """
        self.validate_operands(a, b)
        return a - b

# Multiplication Operation
class Multiplication(Operation):
    """
    Multiply 2 numbers
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute multiplication
        """
        self.validate_operands(a, b)
        return a * b

# Division Operation
class Division(Operation):
    """
    Divide 2 numbers
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validation to make sure b != 0
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute division
        """
        self.validate_operands(a, b)
        return a / b

# Power Operation
class Power(Operation):
    """
    Multiply a number by a power
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        validation to make sure b is not less than 0
        """
        super().validate_operands(a, b)
        if b < 0:
            raise ValidationError("Negative exponents not supported")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute power function
        """
        self.validate_operands(a, b)
        return Decimal(float(a) ** float(b))

# Square root operation
class SQRT(Operation):
    """
    Find the square root of a number
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validation to make sure b is not <= 0
        """
        super().validate_operands(a, b)
        if a < 0:
            raise ValidationError("Cannot calculate root of negative number")
        if b == 0:
            raise ValidationError("Zero root is undefined")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute square root function
        """
        self.validate_operands(a, b)
        return Decimal(pow(float(a), 1 / float(b)))
    
# Modulus Operation
class Modulus(Operation):
    """
    Perform modulus calculation
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """ Validation to make sure b != 0 """

        super().validate_operands(a,b)
        if b == 0:
            raise ValidationError("Cannot calculate modulus with 0 as divisor")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """ Execute modulus operation """

        self.validate_operands(a,b)
        return Decimal(float(a) % float(b))

# Floor Operation
class Floor(Operation):
    """Calculates floor division i.e. (10/3 == 3)"""
    
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """Validate that b != 0"""

        super().validadte_operands(a,b)
        if b == 0:
            raise("Cannot calculate floor division with b = 0")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Execute floor division"""

        self.validate_operands(a,b)
        return Decimal(float(a) // float(b))

# ============================
# Operation Factory
# ============================
class OperationFactory:
    """
    Factory pattern to create operation instances.
    """

    _ops: Dict[str, type] = {
        'add': Addition,
        'subtract': Subtraction,
        'multiply': Multiplication,
        'divide': Division,
        'power': Power,
        'sqrt': SQRT,
        'modulus': Modulus,
        'floor': Floor
    }

    @classmethod
    def register_operation(cls, name: str, ops_class: type[Operation]) -> None:
        """
        Function to dynamically register a new operation type
        """

        if not issubclass(ops_class, Operation):
            raise TypeError("Specific operation must inherit from Operation base class")
        cls._ops[name.lower()] = ops_class

    @classmethod
    def create_operation(cls, operation_type: str) -> Operation: 
        """Create New Operation Instance"""

        ops_class = cls._ops.get(operation_type.lower())
        if not ops_class:
            raise ValueError(f"Unknown operation: {operation_type}")
        return ops_class
