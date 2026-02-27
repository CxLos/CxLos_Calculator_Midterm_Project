"""
Test package for Config module
"""

# =========== Imports =========== #

import pytest
from pathlib import Path
from decimal import Decimal
from tempfile import TemporaryDirectory
from unittest.mock import patch

from app.config.config import Config, fetch_root

# ================ Config Tests =============== #

def test_project_root():
    """Test getting the root directory"""

    root = fetch_root()

    assert isinstance(root, Path)
    assert root.name == "CxLos_Calculator_Midterm_Project"