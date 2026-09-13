# Vectra Testing Strategy & Architecture

## Strategy Overview

Vectra enforces strict automated test verification. Pull requests and commits must pass all test suites before merge.

---

## Test Directory Structure

```
tests/
├── test_lexer.py
├── test_parser.py
├── test_runtime.py
├── test_ece_toolboxes.py
├── test_universal_matrix_commands.py
├── test_help_system.py
├── test_logger.py
└── test_pdf_functions.py
```

---

## Running Tests

Execute pytest from the root repository directory:

```bash
pytest tests/
```

