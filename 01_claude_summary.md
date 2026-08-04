# Stage 1 Summary: Environment Setup & Synthetic Exposure Data

## Environment setup
- Installed Python via Homebrew (or confirmed existing install)
- Created a project folder and a **virtual environment** (`venv`) to isolate this project's packages from system Python
- Learned to verify a venv is active properly (`which python3` pointing inside the project folder) rather than relying on the `(venv)` prompt text, which doesn't always show
- Installed core packages: `pandas`, `numpy`, `jupyter`, `ipykernel`
- Learned the difference between running code via the **Terminal** (consistent, uses your selected interpreter) vs **Code Runner's Output tab** (can silently use a different interpreter, causing confusing "works here, not there" bugs) — and adjusted Code Runner's settings to route through the Terminal instead

## Git & GitHub
- Initialized a git repo via VS Code's Source Control panel
- Created `.gitignore` (to exclude `venv/` and other junk from version control) and a `README.md` outlining the project stages
- Connected the local repo to a GitHub repo (`catastrophe-modelling-qld`)
- Hit and resolved a real authentication issue — GitHub no longer accepts account passwords for git operations, so switched to signing in via VS Code's built-in GitHub account integration rather than personal access tokens
- Successfully pushed the first commit

## Notebooks vs scripts
- Discussed the tradeoffs: `.ipynb` for exploration/visualisation (renders DataFrames as tables, GitHub displays outputs inline — good for a portfolio), `.py` for reusable, production-style logic
- Agreed on a hybrid approach going forward: notebooks for building/inspecting each stage, with reusable logic later moved into `.py` modules
- Set up `01_exposure_exploration.ipynb` and resolved a kernel-selection issue (needed a VS Code window reload after confirming `ipykernel` was properly installed inside the venv)

## Python & pandas concepts
- `range()` is lazy — it describes a sequence but doesn't produce values until you loop over it or wrap it in `list()`
- Building a DataFrame from a **dictionary** (`{"column_name": values}`) is safer than passing a list of arrays, which pandas can misinterpret as rows instead of columns — this was the root cause of an early `AssertionError`
- In a notebook, just typing a variable name on its own line (e.g. `df`) triggers pandas' rich table rendering — `print(df)` only gives plain text
- `.dtypes` to check column types — including a real-world observation that pandas 3.0.5 uses a native `str` dtype rather than the older generic `object` type for text columns
- `.describe()` for a fast statistical sanity check on numeric columns (confirms generated ranges are correct without eyeballing every row)
- `.round(n)` to control decimal precision
- `.to_csv(..., index=False)` to export cleanly — and *why* `index=False` matters (an unnamed index column silently creeps into re-imported data otherwise)

## What was built
A synthetic 10-property QLD exposure dataset (`exposure_data.csv`) with `policy_id`, `latitude`, `longitude`, `construction_type`, and `sum_insured` — validated, cleaned, and exported. This is the foundation Stage 2 (geospatial mapping) will load and build on.
