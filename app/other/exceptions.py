class CalculatorError(Exception):
    """
    Base exception class
    """
    pass

class ValidationError(CalculatorError):
    """
    Input validation error when user input does not meet criteria
    """
    pass

class OperationError(CalculatorError):
    """
    Error raised when there is a failure during one of the calculations
    """
    pass

class ConfigurationError(CalculatorError):
    """
    Error when there is an error with calculator configuratiaon settings.
    """
    pass