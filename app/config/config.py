
# =========== Imports =========== #

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

# =============================== #

def fetch_root() -> Path:
    """
    Function that fetches project's root directory

    Returns:
        root_directory_path
    """

    current_file = Path(__file__)

    print("Parent directory:", current_file.parent.parent.parent)
    return current_file.parent.parent.parent

# fetch_root()

@dataclass
class Config:
    """
    This class manages all configurations required for the calculator including directory paths, history size, auto-save preferences, max input and min input values and default encoding.
    """