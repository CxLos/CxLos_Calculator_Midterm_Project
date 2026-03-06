
# =================== Imports ================= #

import logging
from decimal import Decimal
from app.calculator.calculator import Calculator
from app.calculator.operations import OperationFactory
from app.other.exceptions import OperationError, ValidationError
from app.other.history import AutosaveObserver, LoggingObserver

# ================== REPL ================== #

def repl():
    """
    CLI interface for the calculator.
    """

    try:
        calc = Calculator()
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutosaveObserver(calc))

        print("Calculator booted. Type 'help' for available commands.")

        while True:
            try:
                command = input("\nEnter command: ").lower().strip()

                if command == 'help':
                    print("\nAvailable commands: \n")
                    print("  add, subtract, multiply, divide, power, sqrt, modulus")
                    print("  history - Show history")
                    print("  clear - Clear history")
                    print("  undo - Undo the last calculation")
                    print("  redo - Redo the last calculation")
                    print("  save - Save calculation history")
                    print("  load - Load calculation history")
                    print("  exit - Exit app")
                    continue

                if command == 'exit':
                    try:
                        calc.save_history()
                        print("History saved successfully.")
                    except Exception as e:
                        print(f"Warning: Could not save history: {e}")
                    print("Goodbye!")
                    break

                if command == 'history':
                    history = calc.show_history()
                    if not history:
                        print("No history yet")
                    else:
                        print("\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}")
                    continue

                if command == 'clear':
                    calc.clear_history()
                    print("History cleared")
                    continue

                if command == 'undo':
                    if calc.undo():
                        print("Operation undone")
                    else:
                        print("Nothing to undo")
                    continue

                if command == 'redo':
                    if calc.redo():
                        print("Operation redone")
                    else:
                        print("Nothing to redo")
                    continue

                if command == 'save':
                    try:
                        calc.save_history()
                        print("History saved successfully")
                    except Exception as e:
                        print(f"Error saving history: {e}")
                    continue

                if command == 'load':
                    try:
                        calc.load_history()
                        print("History loaded successfully")
                    except Exception as e:
                        print(f"Error loading history: {e}")
                    continue

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'sqrt', 'modulus']:
                    try:
                        print("\nEnter numbers (or 'cancel' to abort):")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print("Operation canceled")
                            continue
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print("Operation canceled")
                            continue

                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        result = calc.perform_operation(a, b)

                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print(f"\nResult: {result}")
                    except (ValidationError, OperationError) as e:
                        print(f"Error: {e}")
                    except Exception as e:
                        print(f"Unexpected error: {e}")
                    continue

                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\nOperation cancelled")
                continue
            except EOFError:
                print("\nInput terminated. Exiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue

    except Exception as e:
        print(f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise