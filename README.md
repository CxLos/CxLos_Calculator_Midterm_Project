# 📚 CxLos Calculator Midterm Project

## 📝 Project Description

A professional command-line calculator midterm project built with Python, featuring advanced calculation history management, undo/redo functionality, persistent storage, and comprehensive testing.

## 📂 Table of Contents

- [Installation](#-installation)
- [Configuration Setup](#-configuration-setup)
- [Usage Guide](#-usage-guide)
- [Testing](#-testing)
- [CI/CD Pipeline](#-cicd-pipeline)

---

## 📁 Project Structure

```
CxLos_Calculator_Midterm_Project/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
├── .coveragerc                  # Coverage configuration
├── .env                         # Environment variables (create this)
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
│
├── app/                         # Main application package
│   ├── __init__.py
│   ├── calculator/              # Calculator core logic
│   │   ├── __init__.py
│   │   ├── calculator.py       # Calculator class (main orchestrator)
│   │   ├── calculation.py      # Calculation dataclass
│   │   ├── operations.py       # Operation classes & factory
│   │   ├── memento.py          # Memento for undo/redo
│   │   └── repl.py             # Command-line interface
│   │
│   ├── config/                  # Configuration management
│   │   ├── __init__.py
│   │   └── config.py           # Config class with .env loading
│   │
│   └── other/                   # Supporting utilities
│       ├── __init__.py
│       ├── exceptions.py       # Custom exception classes
│       ├── history.py          # Observer pattern implementations
│       └── validator.py        # Input validation logic
│
├── tests/                       # Unit tests
│   ├── calculator_tests/
│   └── other_tests/
│
├── history/                     # Calculation history storage
│   └── calculator_history.csv
│
├── logs/                        # Application logs
│   └── calculator.log
│
└── .github/                     # CI/CD configuration
    └── workflows/
        └── tests.yml           # GitHub Actions workflow
```

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/CxLos/CxLos_Calculator_Midterm_Project.git
   cd CxLos_Calculator_Midterm_Project
   ```

2. **Create and activate a virtual environment:**
   
   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python main.py
   ```

---

## ⚙️ Configuration Setup

### Environment Variables (.env)

Create a `.env` file in the project root directory to customize calculator behavior:

```bash
CALCULATOR_MAX_HISTORY_SIZE=1000
CALCULATOR_AUTO_SAVE=true
CALCULATOR_DEFAULT_ENCODING=utf-8
```

---

## ▶️ Usage Guide

### Starting the Calculator

Run the calculator from the project root:

```bash
python main.py
```

### Available Commands

#### **Arithmetic Operations**
- `add` - Add two numbers
- `subtract` - Subtract second number from first
- `multiply` - Multiply two numbers
- `divide` - Divide first number by second
- `power` - Raise first number to power of second
- `sqrt` - Calculate nth root (e.g., square root with n=2)
- `modulus` - Calculate remainder after division
- `floor` - Floor division (integer division)
- `percentage` - Calculate percentage (a * b / 100)

#### **Other Commands**
- `help` - Display all available commands
- `exit` - Save history and exit application
- `undo` - Undo the last calculation
- `redo` - Redo the last undone calculation
- `history` - Display all calculation history
- `clear` - Clear all calculation history
- `save` - Manually save history to CSV file
- `load` - Reload history from CSV file
---

## 🧪 Testing

The project includes comprehensive unit tests with **90%+ coverage**.

### Running Tests

**Run all tests:**
```bash
pytest
```

**Run tests with coverage report:**
```bash
pytest --cov=app --cov-fail-under=-90
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

The project uses GitHub Actions for continuous integration, automatically running tests on every push and pull request.

**Workflow file**: `.github/workflows/tests.yml`

**Triggered on:**
- Push to `main` branch
- Pull requests to `main`
- Manual workflow dispatch

**Pipeline steps:**
1. Set up Python 3.13 environment
2. Install dependencies from `requirements.txt`
3. Run pytest with coverage
4. Generate coverage reports
5. Fail build if tests fail

**View workflow runs:**
- Navigate to the "Actions" tab in your GitHub repository
- Monitor test results and coverage metrics

---