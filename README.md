# create-python-project

A command-line tool that creates a new Python project from predefined templates, saving you time and effort.

## Motivation

I'm tired of creating a new python project from scratch. Each time I want to create a new project,
I have to copy and paste the same files and folders from other projects of mine.
And there can be many files for a Python project.

Comes this tool. This tool is a CLI tool that creates a new Python project from predefined templates.
Upon completion, the project is ready to be used.

## Usage
```bash
create-python-project [OPTIONS] [DIR]
```
If `DIR` is not provided, a new directory will be created and named `project_name`,
else `DIR` will be used as the project root directory.

To view help and options:
```bash
create-python-project --help
```

**Important note:** This project is not intended to be published on PyPI. There has been another project with the same name on
PyPI from a different author. If you want to use this project, follow the instructions below:

1. Clone this repository
2. Install build dependencies: `pip install build`
3. Run `python -m build`
4. Install the built package: `pip install dist/create_python_project*.whl`
5. Run `create-python-project --help`

## Expected project structure
If `DIR` is provided, the project structure will be:
```
project_root
    .pre-commit-config.yaml
    .gitignore
    README.md
    src
        project_name
            main.py
    pyproject.toml
```

If `DIR` is not provided, the project structure will be:
```
project_root
    project_name
        .pre-commit-config.yaml
        .gitignore
        README.md
        src
            project_name
                main.py
        pyproject.toml
```

## Features
- Creates a Python project structure
- Sets up virtual environment (planned)
- Initializes git repository (planned)
- Configures pre-commit hooks
- Creates basic project files with proper imports
- Generates a pyproject.toml file with project metadata

## Requirements
- click
- jinja2
