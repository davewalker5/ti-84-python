[![Build Status](https://github.com/davewalker5/ti-84-python/workflows/Python%20CI%20Build/badge.svg)](https://github.com/davewalker5/ti-84-python/actions)
[![Coverage](https://codecov.io/gh/davewalker5/ti-84-python/branch/main/graph/badge.svg?token=U86UFDVD5S)](https://codecov.io/gh/davewalker5/ti-84-python)
[![GitHub issues](https://img.shields.io/github/issues/davewalker5/ti-84-python)](https://github.com/davewalker5/Odti-84-pythoneSolver/issues)
[![Releases](https://img.shields.io/github/v/release/davewalker5/ti-84-python.svg?include_prereleases)](https://github.com/davewalker5/ti-84-python/releases)
[![License](https://img.shields.io/badge/License-mit-blue.svg)](https://github.com/davewalker5/ti-84-python/blob/main/LICENSE)
[![Language](https://img.shields.io/badge/language-python-blue.svg)](https://www.python.org)
[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/davewalker5/ti-84-python)](https://github.com/davewalker5/ti-84-python/)


# TI-84 CE-T Python Applications and Experiments

A collection of Python applications, utilities, and coding experiments developed for the TI-84 Plus CE-T Python Edition graphing calculator.

The repository combines small educational programs, practical utilities, and more exploratory projects built within the constraints of the calculator platform. Topics range from mathematics and science tools through to networking calculations, ecological modelling, and acoustic signal analysis.

The aim of the project is not to produce highly polished “apps”, but to explore what can realistically be achieved on a constrained handheld Python environment while keeping the code understandable, portable, and reasonably efficient.

Current areas include:

- Mathematics and science utilities
    - Small calculators and demonstrations
    - Numerical and graphical experiments
    - Educational coding exercises
- Networking tools
    - IPv4 subnetting helpers
    - Network calculation utilities
    - Reusable subnetting library functions
- Seasonal ecological modelling
    - Simplified ODE-based seasonal models adapted for the TI-84 environment
    - Wildlife detectability and seasonality simulations
    - Graphical rendering of seasonal curves directly on the calculator
- Bat call pulse timing analysis
    - Pulse interval and sequence analysis tools
    - Exploration of time-structure analysis for bat recordings
    - Adaptations of desktop workflows for calculator-scale hardware

The repository also serves as an ongoing exploration of:

- Writing efficient Python for limited hardware
- Reducing memory usage and allocation overhead
- Simplifying numerical methods for embedded-style environments
- Building usable interfaces within the TI-84 graphical system

The programs are intentionally self-contained and avoid external dependencies beyond the calculator’s Python environment.

# Getting Started

The primary documentation for the repository, including details of the available applications, calculator deployment, and usage instructions, is provided through the Sphinx documentation. Building the documentation is the best place to start.

To generate the documentation, a virtual environment should be created and the requirements should be installed:

```bash
scripts/make-venv.sh
```

The documentation can then be built using:

```bash
scripts/make-docs.sh
```

The script ensures the environment is set up so that the documentation will build successfully.

Once the build has completed, the built documentation will be in _docs/build/html_ and can be browsed by opening the _index.html_ file in that folder in a browser.

# Authors

- **Dave Walker** - _Initial work_

# Feedback

To file issues or suggestions, please use the [Issues](https://github.com/davewalker5/ti-84-python/issues) page for this project on GitHub.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
