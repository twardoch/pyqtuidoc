# pyqtuidoc

**pyqtuidoc** is a command-line utility designed to streamline working with Qt `.ui` files created by Qt Designer. It leverages the power of PyQt5 to help developers and UI designers inspect, preview, and generate Python code from these UI definition files.

## Target Audience

This tool is primarily for:

*   **Python Developers:** Especially those using PyQt5 (or potentially PySide) for building graphical user interfaces.
*   **UI Designers:** Who create UI layouts in Qt Designer and need to see them in action or hand them off to developers.

## Why Use pyqtuidoc?

`pyqtuidoc` simplifies several common tasks when dealing with `.ui` files:

*   **Quick Previews:** Instantly visualize your `.ui` files without writing boilerplate PyQt5 code.
*   **Code Generation:** While PyQt5's `pyuic5` tool is the standard for converting `.ui` files to Python code, `pyqtuidoc` offers a convenient wrapper with options that can make the process more flexible, especially for quick tests or specific import needs.
*   **Inspection & Debugging:** Helps in understanding the structure of a UI and can be a first step in debugging layout or widget issues.
*   **Custom Widget Support (Basic):** Includes a mechanism (`fakemods`) that can be extended to help Qt's UI compiler locate custom widget classes.

## Features

*   **Load and Preview Qt `.ui` files:** Directly render and display the UI defined in a `.ui` file.
*   **Python Code Generation:** Generate Python code from `.ui` files (leveraging PyQt5's `uic` module).
*   **Flexible Output:** Output generated code to `stdout` or a specified file.
*   **Executable Boilerplate:** Option to generate extra Python code to make the UI directly runnable for testing purposes.
*   **Customizable Code Style:**
    *   Control indentation (spaces or tabs).
    *   Specify import style for resource modules (e.g., `from . import myresource_rc` vs `import myresource_rc`).
*   **Resource File Handling:** Define a custom suffix for generated Python resource files (e.g., `_rc.py`).
*   **Debug Mode:** Verbose output for troubleshooting.

## Installation

### Prerequisites

*   Python 3.7+
*   PyQt5 (`pip install PyQt5`)

### Installing pyqtuidoc

You can install `pyqtuidoc` from PyPI:

```bash
pip install pyqtuidoc
```

Alternatively, for development or to get the latest version, you can clone the repository and install it from source:

```bash
git clone https://github.com/twardoch/pyqtuidoc.git
cd pyqtuidoc
pip install .
```
Or in editable mode:
```bash
pip install -e .
```

## Usage

`pyqtuidoc` is used via the `qtuidocmake` command-line tool.

### Command-Line Interface (CLI)

The basic syntax is:

```bash
qtuidocmake [OPTIONS] <path_to_ui_file>
```

**Arguments:**

*   `path`: (Required) The path to the `.ui` file you want to process.

**Options:**

*   `-p, --preview`: Show a preview of the UI instead of generating code.
    *   Example: `qtuidocmake -p mydialog.ui`
*   `-o, --output FILE`: Write generated Python code to `FILE`. If `FILE` is `-`, output is written to `stdout` (standard output).
    *   Example: `qtuidocmake mydialog.ui -o ui_mydialog.py`
*   `-x, --execute`: Generate extra boilerplate code within the output file to make the UI class directly testable and displayable when the generated Python file is run.
    *   Example: `qtuidocmake mydialog.ui -o ui_mydialog.py -x`
*   `-d, --debug`: Show debug output, providing more verbose information about the process.
*   `-i N, --indent N`: Set the indent width for the generated Python code to `N` spaces. If `N` is `0`, tabs will be used for indentation. Default is `4` spaces.
    *   Example: `qtuidocmake mydialog.ui -o ui_mydialog.py -i 2`
*   `--import-from PACKAGE`: When generating code, use imports for resource files in the style `from PACKAGE import resource_rc`.
    *   Example: `qtuidocmake mydialog.ui --import-from myproject.resources -o ui_mydialog.py`
*   `--from-imports`: A shortcut for `--import-from=.`. This generates resource imports like `from . import resource_rc`. This is useful if your UI files and resource files are part of the same Python package.
    *   Example: `qtuidocmake mydialog.ui --from-imports -o ui_mydialog.py`
*   `--resource-suffix SUFFIX`: Append `SUFFIX` to the basename of resource files when generating import statements. The default suffix is `_rc`. For example, if your `.qrc` file is `icons.qrc`, `pyuic5` might generate `icons_rc.py`, and this option helps form the correct import statement.
    *   Example: `qtuidocmake mydialog.ui --resource-suffix _resources -o ui_mydialog.py`
*   `-v, --verbose`: Increase output verbosity. Can be used multiple times (e.g., `-vv` for more detail).
*   `-V, --version`: Show the program's version number and exit.

### Examples

1.  **Preview a UI file:**
    ```bash
    qtuidocmake --preview assets/my_interface.ui
    ```

2.  **Generate Python code and save it to a file:**
    ```bash
    qtuidocmake assets/my_interface.ui --output src/ui_my_interface.py
    ```

3.  **Generate Python code with 2-space indentation and make it executable for testing:**
    ```bash
    qtuidocmake assets/my_interface.ui --output src/ui_my_interface.py --indent 2 --execute
    ```

4.  **Generate code using relative imports for resources:**
    ```bash
    qtuidocmake assets/my_interface.ui --from-imports --output src/ui_my_interface.py
    ```

## Technical Details

### How it Works

`pyqtuidoc` primarily acts as a user-friendly wrapper around the functionalities provided by `PyQt5.uic`.

*   **UI Loading & Preview:** For previewing (`--preview`), it uses `PyQt5.uic.loadUi()` to dynamically load the UI definition from the `.ui` file into memory and render it using `PyQt5.QtWidgets`.
*   **Code Generation:** For code generation, it utilizes the capabilities of `PyQt5.uic` (similar to the `pyuic5` command-line tool) to parse the `.ui` file (an XML format) and convert it into Python code that defines a class representing the UI. The various command-line options (indentation, import style, etc.) are passed to the underlying `uic` compilation process.
*   **`fakemods` Directory:** The `pyqtuidoc/__main__.py` script adds `pyqtuidoc/fakemods` to `sys.path`. This directory is intended to contain placeholder Python modules. If your `.ui` file references custom widgets that would normally be resolved at runtime through Python imports, Qt's UI compiler might need to find these modules during the code generation phase. The `fakemods` can provide empty or mock versions of these custom widget modules, allowing `uic` to process the `.ui` file successfully even if the full custom widget implementations are not in the `PYTHONPATH` at compile time. Currently, the modules within `fakemods` are empty placeholders and would need to be populated with appropriate class/module structures if complex custom widgets are used.

### Code Structure

*   `pyqtuidoc/`: The main Python package.
    *   `__init__.py`: Initializes the package and stores version information (`__version__`).
    *   `__main__.py`: Contains the command-line interface logic, argument parsing (`argparse`), and the core functionality for previewing or triggering code generation using `PyQt5.uic`.
    *   `fakemods/`: A directory containing empty Python files (e.g., `yselector.py`, `ycheckbutton.py`). These are added to `sys.path` to potentially aid `PyQt5.uic` in resolving custom widget paths referenced in `.ui` files.
*   `setup.py`: The setuptools script used for packaging and distributing `pyqtuidoc`. Contains metadata like author, license, dependencies, and defines the `qtuidocmake` console script entry point.
*   `requirements.txt`: Lists runtime dependencies.
*   `LICENSE`: Contains the MIT license text.
*   `README.md`: This file.

### Dependencies

*   **PyQt5 (>=5.15.4):** Essential for all core functionalities, including parsing `.ui` files, rendering UIs, and generating Python code.
*   **Send2Trash (>=1.5.0):** Listed as a dependency in `requirements.txt`. Its direct use is not immediately apparent in the primary `__main__.py` workflow but might be used in other parts of the project or planned features.

## Contributing

Contributions are welcome! Whether it's bug reports, feature suggestions, or code contributions, please feel free to engage with the project.

### Reporting Bugs

*   Please open an issue on the project's GitHub issue tracker: [https://github.com/twardoch/pyqtuidoc/issues](https://github.com/twardoch/pyqtuidoc/issues)
*   Describe the bug clearly, including steps to reproduce it, the expected behavior, and the actual behavior.
*   Include your `pyqtuidoc` version, Python version, and OS information.

### Setting Up Development Environment

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/twardoch/pyqtuidoc.git
    cd pyqtuidoc
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    Install the runtime dependencies and the package in editable mode:
    ```bash
    pip install -r requirements.txt
    pip install -e .
    ```
4.  **Install development dependencies (if any are specified in `setup.py`'s `extras_require`):**
    ```bash
    pip install -e .[dev]
    ```

### Coding Conventions

*   Follow [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).
*   Keep code clear, concise, and well-commented where necessary.

### Pull Requests

1.  Fork the repository on GitHub.
2.  Create a new branch for your feature or bug fix: `git checkout -b my-new-feature`.
3.  Make your changes and commit them with clear, descriptive messages.
4.  Push your branch to your fork: `git push origin my-new-feature`.
5.  Open a pull request against the main `pyqtuidoc` repository.

## License

`pyqtuidoc` is licensed under the **MIT License**. See the `LICENSE` file for more details.
