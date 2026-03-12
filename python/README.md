# Python Implementation of to24

This directory contains the Python version of the to24 24-game solver.  
It is structured to support multiple independent libraries (like `to24`, `hello`, etc.) and includes helper scripts for environment setup and project scaffolding.

---

## PART 1 — First time using the package

Before you can work on any Python library in this directory, you need to set up a virtual environment.  
Run the following commands (adjust the path to your actual `to24/python` location):

```bash
cd /YOUR_PATH/to24/python
./tool/setup-python.sh
```

**What this script does:**

- Detects your Python version (e.g., 3.14 → `venv314`)
- Creates a virtual environment folder (e.g., `venv314/`)
- Generates an activation helper script `activate.sh` in the current directory
- Configures VSCode workspace settings (`.vscode/settings.json`) with the correct Python interpreter path
- Installs the VSCode Python extension (if `code` command is available)

After the script finishes, your environment is ready, but **not yet activated** – proceed to PART 2.

---

## PART 2 — Activating the Virtual Environment

You need to activate the virtual environment **every time you open a new terminal** to work on any project inside `python/`.

### ✅ Correct way to activate

```bash
source activate.sh
```

After activation, your terminal prompt will show the environment name (e.g., `venv314`), and `python` will point to the interpreter inside the virtual environment.


### ❌ What NOT to do
If you accidentally run the script directly:

```bash
./activate.sh
```
you will see an error message:

```text
❌ Please use `source activate.sh`
```

This is because running it as an executable starts a **subshell**, and any environment changes are lost when the subshell exits. Using `source` executes the script in the **current shell**, preserving the environment.

### 🔍 Verifying activation
To confirm that the virtual environment is active, run:

```bash
which python
```
The output should show a path inside the project directory, e.g.:

```text
/d/code/to24/python/venv314/Scripts/python
```

---

## PART 3 — How to use `create-lib.sh`

The `tool/create-lib.sh` script helps you generate a new Python library project with a standard directory structure.  
It creates a folder named after your library, containing:

- `examples/` – a simple example application
- `tests/` – unit test templates
- `library_name/` – the actual Python package (source code only)
- `setup.py` – installation script in the project root

### Usage example – creating a library called `hello`

```bash
cd /YOUR_PATH/to24/python
./tool/create-lib.sh hello
```

After running this command, the following structure will be created inside `python/`:

```bash
hello/
├── README.md
├── examples/
│   └── app.py*
├── hello/
│   ├── __init__.py
│   ├── algorithm/
│   │   └── __init__.py
│   └── core.py
├── setup.py
└── tests/
    └── test.py*
```

- `hello/examples/app.py` – a minimal demo that uses the library.
- `hello/tests/test.py` – a unittest skeleton.
- `hello/hello/` – the actual package source code.
- `hello/setup.py` – installation script for the library.

You can then `cd hello` and install the library in editable mode:

```bash
cd hello
pip install -e .
```

Now you can import your library from anywhere (as long as the virtual environment is active).

> **Note:** If you use the name `to24` instead of `hello`, the script generates a full 24‑game solver implementation instead of a minimal template.

---

## PART 4 — Using `install-dev.sh` to enter development mode

After activating the virtual environment (see PART 2), you need to install the `to24` kit in editable mode so that your changes are immediately reflected when importing the library. The `tool/install-dev.sh` script automates this process.

### Usage

Simply run the script from anywhere inside the `python/` directory:

```bash
./tool/install-dev.sh
```

The script will:
- Save your current working directory.
- Change to the `to24/` folder (where `setup.py` resides).
- Execute `pip install -e .` to install the package in editable mode.
- Return you to your original directory.

If the virtual environment is not active, the script will warn you and ask for confirmation before proceeding.

After running this script once, the `to24` package is registered in your virtual environment, and you can import it from anywhere (e.g., in `examples/` or `tests/`) while developing.

> **Note:** You only need to run `install-dev.sh` once per virtual environment, unless you delete the virtual environment or change the package name.

---

## PART 5 — Using the `to24` Python library

After activating the virtual environment and installing the package (via `install-dev.sh`), you can use the `to24` solver in your own code.

### Basic usage

```python
from to24 import To24

# Create a solver with the default 'simple' algorithm
solver = To24()

# Check if four numbers can make 24
result = solver.solve(1, 2, 3, 4)
print(result)  # True

# Get the expression as well
result, expr = solver.solve(1, 2, 3, 4, return_expr=True)
print(expr)    # ((1 + 2) + 3) + 4
```

### Switching algorithms

The library supports multiple algorithms. Currently implemented:

- `'simple'` – brute‑force with a fixed parentheses pattern.
- `'person_like'` – placeholder for a human‑like reasoning algorithm.
- `'remove_dup'` – placeholder for duplicate‑expression removal.

To use a different algorithm:

```python
solver = To24(algorithm='person_like')
result = solver.solve(1, 2, 3, 4)   # always False for now (placeholder)
```

### API Reference

#### `class To24(algorithm='simple')`

- **`solve(a, b, c, d, return_expr=False)`**  
  Checks whether the four integers `a, b, c, d` (each between 1 and 10) can be combined with `+`, `-`, `*`, `/` to obtain 24.  
  - If `return_expr` is `False` (default), returns a boolean.  
  - If `return_expr` is `True`, returns a tuple `(bool, str)` where the string is a valid expression if the result is `True`, otherwise an empty string.

### Running the examples

After installation, you can run the example app:

```bash
cd python/to24
python examples/app.py 1 2 3 4
```

Or run the unit tests:

```bash
python tests/test.py
```