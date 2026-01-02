# GitHub Copilot Instructions for This Repository ✅

## Purpose
Short, explicit rules to guide GitHub Copilot suggestions so generated code matches project conventions and is easy to read, maintain, and review.

---

## Quick, must-follow rules 🔧
- **Always write type hints whenever defining a variable.** Use PEP 526 style annotations for variables and annotate function signatures and return types.
- **Avoid ambiguous single-letter names** like `a`, `i`, `j` for meaningful variables. Use descriptive names (`idx_frame`, `count_items`) and reserve single letters only for tiny, local loop counters when truly appropriate.
- **Prefer `type_first` naming with words ordered by importance.** Put a short token implying the variable type first (e.g., `dir_`, `arr_`, `list_`, `html_`, `df_`), then the main concept, then qualifiers. For time/pulse units prefer explicit `ms_` for millisecond values (e.g., `servo_min_ms`, `servo_max_ms`) rather than ambiguous `min_ms`/`max_ms`.
- **Use snake_case** for variables, functions, and methods; PascalCase for classes and types.
- **Boolean names** should start with `is_`, `has_`, `should_` (e.g., `is_ready: bool`).
- **Constants**: use UPPER_SNAKE_CASE and annotate types (e.g., `MAX_EPOCHS: int = 100`).

- **Write type hints whenever defining a variable.** Use PEP 526 style annotations for variables, e.g. `x: int = 0`, `arr_w_mat: np.ndarray = np.zeros((3, 3))`.
- **Never use ambiguous single-letter names** like `a`, `i`, `j` for meaningful variables. Reserve single letters only for tight, clearly-scoped loop indices when unavoidable, and prefer descriptive names even for loops (e.g., `idx_frame`).
- **Prefer `type_first` naming with words ordered by importance.** Put a short token that implies the variable type (e.g., `dir_`, `arr_`, `list_`, `html_`, `df_`) first, then the main concept and then qualifiers.
  - Examples:
    - Prefer `dir_curr` over `curr_dir` for the current directory
    - Prefer `arr_w_mat` over `w_mat` for a W matrix (array)
    - Prefer `list_name_title` over `title_names` for a list of title names
    - Prefer `html_fig_flatness` over `fig_flatness_html` for an HTML string for a flatness figure
- **Use underscores** to separate tokens (snake_case). Keep names concise but descriptive.
- **Type-aware prefixes**: choose prefix tokens that give quick type hints (e.g., `str_`, `pos_`, `list_`, `dict_`, `arr_`, `np_`, `df_`, `html_`). Prefer `pos_` for integer positional values (e.g., `pos_center`, `pos_channel`) instead of `int_` because the type is already declared in annotations. Use standard domain-shorteners (e.g., `img_` for image) where appropriate.

---

## Why this style? 💡
Putting a short type token first and ordering words by importance improves readability (especially in parameter lists and class constructors) and makes it easier to scan types and intent when reading or auto-completing code.

---

## Examples 🔍

Before:
```py
cur_dir = os.getcwd()
w_mat = np.zeros((3,3))
title_names = ["A", "B"]
fig_flatness_html = "<div>...</div>"
```

After (preferred):
```py
from typing import List
import numpy as np

# variable annotations included
dir_curr: str = os.getcwd()
arr_w_mat: np.ndarray = np.zeros((3, 3))
list_name_title: List[str] = ["A", "B"]
html_fig_flatness: str = "<div>...</div>"
```

---

## Small, additional suggestions
- For function signatures and class __init__, prefer explicit type annotations for parameters and return types.
- If a complex type is used (e.g., numpy arrays, pandas DataFrame), include the type (e.g., `np.ndarray`, `pd.DataFrame`) in the annotation and, when helpful, add a short inline comment describing shape or units.
- Keep lines short and prioritize readability over extreme brevity.


---

If you (Copilot) propose code that violates these rules, prefer the style in this file instead and add or correct type hints and names automatically.
