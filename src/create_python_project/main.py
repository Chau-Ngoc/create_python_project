import re
from pathlib import Path

import click
from jinja2 import Environment, PackageLoader, TemplateNotFound, select_autoescape

from create_python_project.renderer import TemplateRenderer
from create_python_project.utils import render_to_file

templates_dir = "templates"
env = Environment(loader=PackageLoader("create_python_project", templates_dir), autoescape=select_autoescape())
tpl_renderer = TemplateRenderer(env)


def create_default_project_path(ctx, param, value):
    if value is None:
        return Path.cwd()
    else:
        return value


@click.command()
@click.argument(
    "dest", required=False, type=click.Path(exists=True, file_okay=False), callback=create_default_project_path
)
@click.option("--author_name", help="The name of the author", prompt="Name of the project's author")
@click.option("--author_email", help="The email of the author", prompt="Email of the project's author")
@click.option(
    "--project_name",
    help="The name of the project. This will also be used to name your project root directory. Spaces will be replaced by underscores.",
    prompt="Project name",
)
@click.option(
    "--project_version",
    help="The version of the project",
    default="0.1.0",
    show_default=True,
    prompt="Project version",
)
def cli(author_name, author_email, project_name, project_version, dest):
    """Create a new Python project in DEST

    DEST is the destination directory. If not specified, a new directory named PROJECT_NAME will be created in the
    current directory, and the project will be created in it. Else, the project will be created in DEST."""
    project_name = re.sub(r"\s+", "_", project_name)

    if dest == Path.cwd():
        dest = (dest / project_name).resolve()
        dest.mkdir(exist_ok=False)
    else:
        dest = Path(dest).resolve()

    try:
        main_path = dest / "src" / project_name
        main_path.mkdir(parents=True)
        render_to_file(
            tpl_renderer,
            "main.py.jinja",
            main_path / "main.py",
            author_name=author_name,
        )

        render_to_file(
            tpl_renderer,
            "pyproject.toml.jinja",
            dest / "pyproject.toml",
            project_name=project_name,
            project_version=project_version,
            author_name=author_name,
            author_email=author_email,
        )
        render_to_file(tpl_renderer, ".gitignore.jinja", dest / ".gitignore")
        render_to_file(tpl_renderer, ".pre-commit-config.yaml.jinja", dest / ".pre-commit-config.yaml")
        render_to_file(tpl_renderer, "README.md.jinja", dest / "README.md")

    except (TemplateNotFound, FileExistsError) as e:
        click.secho(e, err=True, fg="red")
        click.get_current_context().exit(111)

    click.secho(f'New project is created in "{dest}"', fg="green")
