# GitHub Copilot Custom Instructions

This project follows strict Python development standards. All code suggestions should adhere to the following rules:

## 1. Style & Formatting
- **PEP 8 Compliance:** Strictly follow PEP 8 guidelines for indentation (4 spaces), spacing, and line lengths.
- **Imports:** Organize imports into three sections: standard library, third-party packages, and local modules.

## 2. Type Safety
- **Mandatory Type Hints:** Always include type hints for every variable definition, function argument, and return type.
- **Syntax:** - Use `variable_name: type = value` for assignments.
  - For Python 3.10+, use the pipe operator `|` for unions (e.g., `int | None`) instead of `Optional`.

## 3. Naming Conventions
- **No Ambiguous Names:** Avoid single-letter variables (e.g., `x`, `y`, `i`). Use descriptive names that convey intent (e.g., `index`, `user_record`).
- **Boolean Prefixes:** All boolean variables and functions returning booleans must start with an affirmative prefix:
  - `is_` (e.g., `is_valid: bool`)
  - `has_` (e.g., `has_access: bool`)
  - `should_` (e.g., `should_process: bool`)

## 4. Documentation
- **Docstrings:** Use Google-style docstrings for all modules, classes, and functions.
- **Clarity:** Code should be self-documenting, but complex logic requires concise inline comments.
