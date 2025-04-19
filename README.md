# Command line signature
```bash
create-python-project [OPTIONS] [DIR]
```
If `DIR` is not provided, a new directory will be created and named `project_name`,
else `DIR` will be used as the project root directory.

# Template project structure

```
project_root
    .git
    .venv
    .pre-commit-config.yaml
    .gitignore
    src
        project_name
            main.py
    tests
        project_name
            test_main.py
    pyproject.toml
```
