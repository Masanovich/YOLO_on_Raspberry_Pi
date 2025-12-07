````markdown
# GitHub Copilot / Assistant Instructions for YOLO_camera

Purpose
-------
This document provides concise, project-specific instructions for GitHub Copilot (or any assistant) when generating or modifying code in this repository. Follow these guidelines to keep code consistent, safe, and easy to review.

Project overview
----------------
- Language: Python 3.10+ (use the project's virtual environment `.venv` when running tools).
- Main concerns: real-time camera capture, YOLO model inference (ultralytics), Jupyter notebooks for experimentation.

Formatting & style
------------------
- Follow PEP 8 and the project's Ruff configuration. Default line length: 88 characters.
- Use the `charliermarsh.ruff` formatter in VS Code when generating `.py` files. Prefer `ruff --fix` only for `.py` files; do NOT auto-fix `.ipynb` files.
- Use `isort` with `profile = "black"` for import ordering when creating or updating `.py` files.
- When generating code examples for notebooks, be succinct and idiomatic; prefer explicit imports and small helper functions.

Variable naming and type hints
-----------------------------
- Use variable names that indicate the variable's type at a glance. Preferred patterns in this project:
  - `path_file` instead of `file_path`
  - `dir_output` instead of `output_dir`
  - `arr_w_matrix` instead of `matrix_w`
  These conventions help readers quickly identify the kind of value (path, directory, array/matrix, etc.).
- Add appropriate type hints to variables, function parameters, and return types wherever possible. Prefer explicit typing for public functions and library-like helpers. Examples:

```python
path_file: Path = Path("../images/squirrel.jpg")
dir_output: Path = path_file.parent / "output"
arr_w_matrix: np.ndarray

def load_image(path_file: Path) -> np.ndarray:
    ...
```

 - When type hinting notebooks, keep annotations clear but concise; it's acceptable to use `# type:` comments for inline clarity when needed.

Notebooks (.ipynb)
-------------------
- Do NOT remove imports or perform other destructive fixes for `.ipynb` files unless explicitly instructed by the user. Notebooks are used interactively and may require different behavior than `.py` modules.
- Avoid large automatic refactors in notebooks. If formatting is needed, prefer using the repository script `scripts/strip_notebook_blanks.py` to remove leading blank lines, or suggest pairing notebooks with `jupytext` for `.py`-backed formatting.
- Prefer providing small, self-contained cells rather than long scripts pasted into a single cell.

Virtual environments & dependencies
----------------------------------
- Use `.venv` for local testing. Do not modify `.venv` files in the repo.
- When suggesting new dependencies, add them to `requirements.txt` (or propose `pyproject.toml`) and explain why.

Hardware and side effects
-------------------------
- Code that opens camera devices (e.g., `cv2.VideoCapture`) must always ensure the device is released on error or interruption. Use context managers or `try/finally` blocks.
- Avoid long-running blocking loops in notebook cells. Suggest non-blocking alternatives or helper scripts that run outside the notebook when appropriate.

Model files, data, and large artifacts
------------------------------------
- Do not add large model weights or dataset files to the repository. Use `weights/`, `runs/`, or `output/` directories which are listed in `.gitignore`.
- When demonstrating model usage, reference placeholder paths (e.g., `yolov8s.pt`) and document where to place real files.

Security and secrets
--------------------
- Never add API keys, credentials, or secrets into source files or notebooks. If credentials are required, instruct the user to store them in environment variables or a `.env` file (do NOT generate `.env` with secrets checked in).

Tests and CI
-----------
- When adding or changing logic, include unit tests where reasonable. Prefer small, fast tests that do not require GPU hardware.
- For suggested CI changes — provide a minimal, clearly-explained YAML snippet and explain required secrets and runner constraints.

Prompts and code generation guidance
-----------------------------------
When asked to generate code for this repository, follow this pattern in your output:

1. Short summary (1-2 lines) of what you'll add or change.
2. A small plan of steps when the change is non-trivial.
3. The code changes themselves, minimal and targeted — prefer adding new files rather than editing many unrelated files.
4. A brief verification guide (commands to run, expected output).

Examples
--------
- Good prompt for generating a helper:
  "Add a small `utils/camera.py` helper with a context manager that opens and safely releases `cv2.VideoCapture`, and update the camera notebook to import and use it. Include a short test snippet." 

- Bad prompt (avoid):
  "Refactor the whole repo to use async IO everywhere." (too broad; ask for a focused change instead)

Commit messages and PRs
----------------------
- Write concise commit messages in imperative mood (e.g., "Add camera context manager").
- For PR descriptions, include a short summary, rationale, and testing steps.

When in doubt
-------------
- Ask the user for clarification rather than making large automated changes. If a requested change might break experiments or notebooks, produce an opt-in patch and explain the risk.

Contact / metadata
------------------
- Repo root path: `/home/masayuki/Documents/Projects/Python/YOLO_camera`
- Primary developer: masayuki (local machine). For any risky or destructive changes, request explicit approval.

---
This file is intended as human-readable guidance for Copilot or assistants working in this repository. It is not enforced by tooling; please follow it as best practice.

````
