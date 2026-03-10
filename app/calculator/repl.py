
# =================== Imports ================= #

import logging
from decimal import Decimal
import colorama
from colorama import Fore, Back, Style
from app.calculator.calculator import Calculator
from app.calculator.operations import OperationFactory
from app.other.exceptions import OperationError, ValidationError
from app.other.history import AutosaveObserver, LoggingObserver

colorama.init(autoreset=True)

# ================== REPL ================== #

def repl():
    """
    CLI interface for the calculator.
    """

    try:
        calc = Calculator()
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutosaveObserver(calc))

        print(f"{Fore.GREEN}Calculator booted. Type 'help' for available commands.{Style.RESET_ALL}")

        while True:
            try:
                command = input(f"\n{Fore.LIGHTYELLOW_EX}Enter command: {Style.RESET_ALL}").lower().strip()

                if command == 'help':
                    print(f"\n{Fore.GREEN}Available commands: \n{Style.RESET_ALL}")
                    print("  add, subtract, multiply, divide, power, sqrt, modulus, floor, percentage")
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
                        print(f"{Fore.GREEN}History saved successfully{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Warning: Could not save history: {e}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                    break

                if command == 'history':
                    history = calc.show_history()
                    if not history:
                        print(f"{Fore.YELLOW}No history yet{Style.RESET_ALL}")
                    else:
                        print(f"\n{Fore.GREEN}Calculation History:{Style.RESET_ALL}")
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}")
                    continue

                if command == 'clear':
                    calc.clear_history()
                    print(f"{Fore.GREEN}History cleared{Style.RESET_ALL}")
                    continue

                if command == 'undo':
                    if calc.undo():
                        print(f"{Fore.GREEN}Operation undone{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}Nothing to undo{Style.RESET_ALL}")
                    continue

                if command == 'redo':
                    if calc.redo():
                        print(f"{Fore.GREEN}Operation redone{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}Nothing to redo{Style.RESET_ALL}")
                    continue

                if command == 'save':
                    try:
                        calc.save_history()
                        print(f"{Fore.GREEN}History saved successfully{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Error saving history: {e}{Style.RESET_ALL}")
                    continue

                if command == 'load':
                    try:
                        calc.load_history()
                        print(f"{Fore.GREEN}History loaded successfully{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Error loading history: {e}{Style.RESET_ALL}")
                    continue

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'sqrt', 'modulus', 'floor', 'percentage']:
                    try:
                        print(f"{Fore.LIGHTMAGENTA_EX}\nEnter numbers (or 'cancel' to abort):{Style.RESET_ALL}")
                        a = input(f"{Fore.LIGHTMAGENTA_EX}First number: {Style.RESET_ALL}")
                        if a.lower() == 'cancel':
                            print(f"{Fore.YELLOW}Operation canceled{Style.RESET_ALL}")
                            continue
                        b = input(f"{Fore.LIGHTMAGENTA_EX}Second number: {Style.RESET_ALL}")
                        if b.lower() == 'cancel':
                            print(f"{Fore.YELLOW}Operation canceled{Style.RESET_ALL}")
                            continue

                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        result = calc.perform_operation(a, b)

                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print(f"{Fore.CYAN}\nResult: {result}{Style.RESET_ALL}")
                    except (ValidationError, OperationError) as e:
                        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
                    continue

                print(f"{Fore.RED}Unknown command: '{command}'. Type 'help' for available commands.{Style.RESET_ALL}")

            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Operation cancelled{Style.RESET_ALL}")
                continue
            except EOFError:
                print(f"\n{Fore.YELLOW}Input terminated. Exiting...{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
                continue

    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise